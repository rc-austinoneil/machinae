import io
import json
from defang import defang

import sys
sys.setrecursionlimit(10000)

class bcolors:
    '''Class for coloring terminal output'''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class MachinaeOutput:
    @staticmethod
    #pylint: disable=no-else-return, redefined-builtin, inconsistent-return-statements
    #Will be cleaned up in upcoming refactor
    def get_formatter(format):
        if format.upper() == "N":
            return NormalOutput()
        elif format.upper() == "J":
            return JsonOutput()
        elif format.upper() == "D":
            return DotEscapedOutput()
        elif format.upper() == "S":
            return ShortOutput()

    @staticmethod
    def escape(text):
        return str(text)

    #pylint: disable=attribute-defined-outside-init
    #Will be cleaned up in upcoming refactor
    def init_buffer(self):
        self._buffer = io.StringIO()

    def print(self, line, lf=True):
        self._buffer.write(line)
        if lf:
            self._buffer.write("\n")


class NormalOutput(MachinaeOutput):
    def output_header(self, target, otype, otype_detected):
        self.print(bcolors.HEADER + "-" * 50)
        self.print(" Information for {0}".format(self.escape(target)))
        self.print(" Observable type: {0} (Auto-detected: {1})".format(otype, otype_detected))
        self.print("-" * 50 + bcolors.ENDC)

    def run(self, result_sets: object):
        self.init_buffer()
        #pylint: disable=too-many-nested-blocks
        for row in result_sets:
            (target, otype, otype_detected) = row.target_info

            self.output_header(target, otype, otype_detected)
            self.print("")

            for item in row.results:
                site = item.site_info
                if hasattr(item, "error_info"):
                    self.print(bcolors.ERROR + "[!] Error from {0}: {1}".format(site["name"], item.error_info) + bcolors.ENDC)
                    continue

                if not item.resultset:
                    self.print(bcolors.WARNING + "[-] No {0} Results".format(site["name"]) + bcolors.ENDC)
                else:
                    self.print(bcolors.OKGREEN + "[+] {0} Results".format(site["name"]) + bcolors.ENDC )
                    for result in item.resultset:
                        labels = getattr(result[0], "labels", None)
                        if len(result[0].values()) > 1 or labels is not None:
                            values = map(repr, result[0].values())
                            values = map(self.escape, values)
                            if labels is not None:
                                values = zip(labels, values)
                                values = ["{0}: {1}".format(label, value) for (label, value) in values]
                                output = ", ".join(values)

                            if result[1] is not None:
                                output = "({0})".format(", ".join(values))
                                output = defang(output)
                        else:
                            output = self.escape(list(result[0].values())[0])
                            output = defang(output)
                        if result[1] is not None:
                            output = "{1}: {0}".format(output, result[1])
                            output = defang(output)
                        self.print("    [-] {0}".format(output))

        return self._buffer.getvalue()


class DotEscapedOutput(NormalOutput):
    escapes = {
        # ".": "\u2024",
        # ".": "<dot>",
        # ".": " DOT ",
        ".": "[.]",
        "@": " AT ",
        "http://": "hxxp://",
        "https://": "hxxps://",
    }

    def output_header(self, target, otype, otype_detected):
        super().output_header(target, otype, otype_detected)
        self.print("* These characters are escaped in the output below:")
        for (find, replace) in self.escapes.items():
            self.print("* '{0}' replaced with '{1}'".format(find, replace))
        self.print("* Do not click any links you find below")
        self.print("*" * 80)

    @classmethod
    def escape(cls, text):
        text = super(DotEscapedOutput, cls).escape(text)
        for (find, replace) in cls.escapes.items():
            text = text.replace(find, replace)
        return text

#pylint: disable=no-self-use, unused-variable
#Will be cleaned up in upcoming refactor
class JsonGenerator(MachinaeOutput):
    def run(self, result_sets):
        records = list()
        for row in result_sets:
            (target, otype, otype_detected) = row.target_info

            for item in row.results:
                output = dict()
                output["site"] = item.site_info["name"]
                output["results"] = dict()
                output["observable"] = target
                output["observable type"] = otype
                output["observable type detected"] = otype_detected

                if hasattr(item, "error_info"):
                    output["results"] = {"error_info": str(item.error_info)}
                elif item.resultset:
                    for result in item.resultset:
                        if result.pretty_name not in output["results"]:
                            output["results"][result.pretty_name] = list()
                        values = list(result.value.values())
                        if len(values) == 1:
                            output["results"][result.pretty_name].append(values[0])
                        elif len(values) > 1:
                            output["results"][result.pretty_name].append(values)
                    for (k, v) in output["results"].items():
                        if len(v) == 1:
                            output["results"][k] = v[0]
                records.append(output)
        return records


class JsonOutput(JsonGenerator):
    def run(self, result_sets):
        self.init_buffer()

        for record in super().run(result_sets):
            self.print(json.dumps(record))

        return self._buffer.getvalue()


class ShortOutput(MachinaeOutput):
    def run(self, result_sets):
        self.init_buffer()

        for row in result_sets:
            (target, otype, otype_detected) = row.target_info
            self.print("[+] {0}".format(target))

            for item in row.results:
                site = item.site_info
                if hasattr(item, "error_info"):
                    self.print("    {0}: Error".format(site["name"]))
                elif not item.resultset:
                    self.print("    {0}: No".format(site["name"]))
                else:
                    self.print("    {0}: Yes".format(site["name"]))

        return self._buffer.getvalue()