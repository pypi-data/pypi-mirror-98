from commandline_lib import exceptions
from commandline_lib import history
from commandline_lib import style


class BaseShell:
    COMMAND_GUIDANCE = ">>>"
    WELCOME_MESSAGE = ""
    history = history.HistoryTable()
    IS_ECHO_WELCOME_MESSAGE = True

    def __init__(self):
        self.prompt_style = style.BaseStyle()
        self.style = style.BaseStyle()

    def set_style(self, style_object):
        self.style = style_object

    def echo(self, *args, sep=",", end="\n", style_obj=None):
        if style_obj is None:
            style_obj = self.style
        index = 0
        for i in args:
            index += 1
            style_obj.echo(str(i))
            if index != len(args):
                style_obj.echo(sep)

        style_obj.echo(end)

    def input(self, style_obj=None):
        if style_obj is None:
            style_obj = self.style
        return style_obj.input()[:-1]

    def parse(self, value: str = None):
        pass

    def get_guidance(self):
        return self.COMMAND_GUIDANCE

    def get_welcome_message(self):
        return self.WELCOME_MESSAGE

    def get_command(self):
        self.echo(self.get_guidance(), style_obj=self.prompt_style, end="")
        s = self.prompt_style.input()[:-1]
        return s

    def keyboard_interrupt_action(self):
        return True

    def program_need_quit_action(self):
        return True

    def user_need_quit_action(self):
        return True

    def other_error_except(self):
        return True

    def can_not_find_error(self):
        return True

    def run(self):
        if self.IS_ECHO_WELCOME_MESSAGE:
            self.echo(self.get_welcome_message())
        while True:
            value = self.get_command()
            try:
                self.parse(value)
            except exceptions.ProgramNeedQuitException:
                flag = self.program_need_quit_action()
                if flag is None:
                    continue
                else:
                    break
            except exceptions.UserNeedQuitException:
                flag = self.user_need_quit_action()
                if flag is None:
                    continue
                else:
                    break
            except KeyboardInterrupt:
                flag = self.keyboard_interrupt_action()
            except:
                flag = self.other_error_except()
            else:
                flag = self.can_not_find_error()
            if flag:
                self.history.append(value)
