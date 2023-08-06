"""
Source Thumbnailer

© 2020-2021 Zander Brown <zbrown@gnome.org>

GPL-3.0-or-later
"""

from __future__ import annotations

from typing import List, Optional, Tuple

import gi
from cairo import (
    Content,
    Context,
    Format,
    ImageSurface,
    RecordingSurface,
    Rectangle,
    Surface,
    SVGSurface,
)

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
gi.require_version("Rsvg", "2.0")

from gi.repository import Gio, GLib, Pango, PangoCairo, Rsvg
from pkg_resources import resource_filename

__version__ = "0.3.1"


def path(name: str) -> str:
    return resource_filename("gnome_source_thumbnailer", "resources/" + name)


class FileThumbnail(Gio.Application):
    types = {
        "application-x-desktop": "#2ec27e",
        "application-x-gtk-builder": "#33d17a",
        "application-json": "#865e3c",
        "application-x-php": "#1a5fb4",
        "text-css": "#1a5fb4",
        "text-html": "#1a5fb4",
        "text-markdown": "#241f31",
        "text-plain": "#000000",
        "text-rust": "#a51d2d",
        "text-sql": "#c64600",
        "text-x-authors": "#9a9996",
        "text-x-changelog": "#9a9996",
        "text-x-chdr": "#1a5fb4",
        "text-x-copying": "#9a9996",
        "text-x-cpp": "#1c71d8",
        "text-x-csrc": "#1a5fb4",
        "text-x-cmake": "#bf2029",
        "text-x-dbus-service": "#2ec27e",
        "text-x-gettext-translation": "#f66151",
        "text-x-gettext-translation-template": "#f66151",
        "text-x-javascript": "#1a5fb4",
        "text-x-log": "#62a0ea",
        "text-x-makefile": "#63452c",
        "text-x-meson": "#39207c",
        "text-x-patch": "#33d17a",
        "text-x-python": "#1a5fb4",
        "text-x-readme": "#9a9996",
        "text-x-ruby": "#f66151",
        "text-x-script": "#5e5c64",
        "text-x-vala": "#613583",
        "text-xml": "#1a5fb4",
    }
    type_alias = {
        "text-javascript": "text-x-javascript",
        "text-x-python3": "text-x-python",
        "text-x-c++": "text-x-cpp",
        "text-x-c++hdr": "text-x-chdr",
        "text-x-c++src": "text-x-cpp",
        "text-x-c": "text-x-csrc",
        "text-x-js": "text-x-javascript",
        "text-x-markdown": "text-x-markdown",
        "text-x-php-source": "application-x-php",
        "text-x-php": "application-x-php",
        "text-x-sh": "text-x-script",
        "text-x-shellscript": "text-x-script",
        "text-x-sql": "text-sql",
        "application-sql": "text-sql",
        "application-javascript": "text-x-javascript",
        "application-x-glade": "application-x-gtk-builder",
        "application-x-javascript": "text-x-javascript",
        "application-x-ruby": "text-x-ruby",
        "application-x-php-source": "application-x-php",
        "application-x-python": "text-x-python",
        "application-x-python3": "text-x-python",
        "application-x-shellscript": "text-x-script",
        "application-xml": "text-xml",
        "application-xml-external-parsed-entity": "text-xml",
    }

    def __init__(self) -> None:
        super().__init__(
            application_id="org.gnome.zbrown.SourceThumbnailer",
            flags=Gio.ApplicationFlags.HANDLES_OPEN | Gio.ApplicationFlags.NON_UNIQUE,
        )
        self.add_main_option(
            "size",
            "s".encode("utf-8")[0],
            GLib.OptionFlags.NONE,
            GLib.OptionArg.INT,
            "Size to Generate",
            "SIZE",
        )
        self.add_main_option(
            "svg",
            0,
            GLib.OptionFlags.NONE,
            GLib.OptionArg.FILENAME,
            "Also export SVG",
            "NAME",
        )
        self.add_main_option(
            "gen-keyfile",
            0,
            GLib.OptionFlags.HIDDEN,
            GLib.OptionArg.NONE,
            "Generate thumbnailer definition",
            None,
        )

    def make_rect(self, x: float, y: float, w: float, h: float) -> Rsvg.Rectangle:
        rect = Rsvg.Rectangle()
        rect.x = x
        rect.y = y
        rect.width = w
        rect.height = h
        return rect

    def whole_rect(self) -> Rsvg.Rectangle:
        return self.make_rect(0, 0, self.dim.width, self.dim.height)

    def calc_text_area(self) -> None:
        rect = self.whole_rect()
        (r, i, self.text_area) = self.base_icon.get_geometry_for_layer("#mask", rect)

    def calc_icon_area(self) -> None:
        rect = self.whole_rect()
        (r, i, self.icon_area) = self.base_icon.get_geometry_for_layer("#mime", rect)

    def recording_surface(self) -> Surface:
        rect = Rectangle(0, 0, self.dim.width, self.dim.height)
        return RecordingSurface(Content.COLOR_ALPHA, rect)

    def do_startup(self) -> None:
        Gio.Application.do_startup(self)

        self.base_icon = Rsvg.Handle.new_from_file(path("base.svg"))
        self.dim = self.base_icon.get_dimensions()

        self.text_mask = self.recording_surface()
        ctx = Context(self.text_mask)
        self.base_icon.render_cairo_sub(ctx, "#mask")
        self.calc_text_area()

        self.icon_mask = self.recording_surface()
        ctx = Context(self.icon_mask)
        self.base_icon.render_cairo_sub(ctx, "#mime")
        self.calc_icon_area()

        self.monospace = Pango.FontDescription("monospace 30")
        self.attrs = Pango.AttrList()
        color = Pango.Color()
        color.parse("#3d3846")
        self.attrs.insert(Pango.attr_foreground_new(color.red, color.green, color.blue))

    def do_activate(self) -> None:
        print("Source Thumbnailer {}".format(__version__))
        print("gnome-source-thumbnailer [file-uri] [output-png]")

    def do_handle_local_options(self, options: GLib.VariantDict) -> int:
        options = options.end().unpack()
        if "size" in options:
            self.size = options["size"]
        else:
            self.size = 64
        if "svg" in options:
            self.svg_name = Gio.File.new_for_commandline_arg(
                bytes(options["svg"][:-1])
            ).get_path()
        else:
            self.svg_name = None
        if "gen-keyfile" in options:
            thumbnailer = GLib.KeyFile.new()
            thumbnailer.set_string(
                "Thumbnailer Entry", "TryExec", "gnome-source-thumbnailer"
            )
            thumbnailer.set_string(
                "Thumbnailer Entry", "Exec", "gnome-source-thumbnailer %u %o --size %s"
            )
            mimes = []
            for t in self.types.keys():
                mimes.append("/".join(t.split("-", 1)))
            for t in self.type_alias.keys():
                mimes.append("/".join(t.split("-", 1)))
            mimes.sort()
            thumbnailer.set_string_list("Thumbnailer Entry", "MimeType", mimes)
            thumbnailer.save_to_file("gnome-source-thumbnailer.thumbnailer")
            return 0
        return -1

    def read_content(self, file: Gio.File) -> List[str]:
        lines = []
        try:
            source = Gio.DataInputStream.new(file.read())
            for i in range(0, 12):
                (data, l) = source.read_line_utf8()
                if data is None:
                    break
                lines.append(data)
        except GLib.Error as e:
            print("Failed to read file: ", e.message)
            self.quit()
        return lines

    def text_surface(self, lines: List[str]) -> Surface:
        surface = self.recording_surface()
        ctx = Context(surface)
        ctx.move_to(self.text_area.x, self.text_area.y)
        layout = PangoCairo.create_layout(ctx)
        layout.set_font_description(self.monospace)
        layout.set_text("\n".join(lines))
        layout.set_attributes(self.attrs)
        PangoCairo.show_layout(ctx, layout)
        return surface

    def pick_icon(self, file: Gio.File) -> Tuple[str, str]:
        info = file.query_info(
            "standard::content-type,standard::symbolic-icon",
            Gio.FileQueryInfoFlags.NONE,
            None,
        )
        names = info.get_symbolic_icon().get_names()
        for name in names:
            if name in self.type_alias:
                name = self.type_alias[name]
            if name in self.types:
                return (name, self.types[name])
        return ("text-x-generic", "#deddda")

    def parse_hex(self, colour: str) -> Tuple[float, float, float]:
        r = int(colour[1:3], 16) / 255
        g = int(colour[3:5], 16) / 255
        b = int(colour[5:7], 16) / 255
        return (r, g, b)

    def mime_surface(self, name: str) -> Surface:
        surface = self.recording_surface()
        ctx = Context(surface)
        mime_icon = Rsvg.Handle.new_from_file(path("{}-symbolic.svg".format(name)))
        x = self.icon_area.x + 8
        y = self.icon_area.y + 8
        w = self.icon_area.width - 16
        h = self.icon_area.height - 16
        area = self.make_rect(x, y, w, h)
        mime_icon.render_document(ctx, area)
        return surface

    def icon_surface(self, file: Gio.File) -> Optional[Surface]:
        surface = self.recording_surface()
        ctx = Context(surface)
        (name, colour) = self.pick_icon(file)
        if name == "text-plain" or name == "text-x-generic":
            return None
        (r, g, b) = self.parse_hex(colour)
        ctx.set_source_rgb(r, g, b)
        ctx.paint()
        if (((r * 255) * 0.299) + ((g * 255) * 0.587) + ((b * 255) * 0.114)) > 160:
            (r, g, b) = self.parse_hex("#3d3846")
        else:
            (r, g, b) = self.parse_hex("#ffffff")
        ctx.set_source_rgb(r, g, b)
        ctx.mask_surface(self.mime_surface(name))
        return surface

    def save_png(self, thumb: Surface, dest: Gio.File) -> None:
        surface = ImageSurface(Format.ARGB32, self.size, self.size)
        ctx = Context(surface)
        scale = self.size / self.dim.height
        ctx.scale(scale, scale)
        ctx.set_source_surface(thumb)
        ctx.paint()
        surface.write_to_png(dest.get_path())

    def do_open(self, files: List[Gio.File], n: int, hint: str) -> None:
        if len(files) != 2:
            print("Expected 2 files, [input] [output]")
            return

        lines = self.read_content(files[0])
        with SVGSurface(self.svg_name, self.dim.width, self.dim.height) as surface:
            ctx = Context(surface)
            self.base_icon.render_cairo(ctx)
            ctx.set_source_surface(self.text_surface(lines))
            ctx.mask_surface(self.text_mask)
            icon = self.icon_surface(files[0])
            if icon:
                ctx.set_source_surface(icon)
                ctx.mask_surface(self.icon_mask)
            self.save_png(surface, files[1])


def main() -> None:
    import sys

    app = FileThumbnail()
    sys.exit(app.run(sys.argv))
