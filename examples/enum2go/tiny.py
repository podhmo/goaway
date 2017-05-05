from goaway.writer import Writer, EnumWriter


class TinyEnumWriter(EnumWriter):
    def write(self, enum, file, m):
        self.write_definition(enum, file, m)
        return m


class TinyWriter(Writer):
    enum_writer_factory = TinyEnumWriter
