from robot.api import ResultVisitor


class KeywordResults(ResultVisitor):

    def __init__(self, results, ignore_lib, ignore_type):
        self.test = None
        self.result = results
        self.ignore_library = ignore_lib
        self.ignore_type = ignore_type

    def start_test(self, test):
        self.test = test

    def end_test(self, test):
        self.test = None

    def start_keyword(self, kw):
        suite = self.test.parent if self.test is not None else ''

        # Ignore library keywords
        keyword_library = kw.libname

        if not keyword_library is None:
            pass
        else:
            keyword_library = ''

        if any(library in keyword_library for library in self.ignore_library):
            pass
        else:
            keyword_type = kw.type
            if any(library in keyword_type for library in self.ignore_type):
                pass
            else:
                keyword_library = kw.libname
                kw_name = kw.name
                if not keyword_library is None:
                    full_name = kw_name
                else:
                    full_name = str(suite) + "." + str(kw_name)
                kw_list = [full_name, str(kw.status), str(kw.elapsedtime / float(1000))]
                self.result.append(kw_list)