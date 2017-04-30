from tkinter import *
import string

class App(object):
    def load_tk(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack()
        
        self.root.bind('<Button-1>', lambda event: self.button1(event))
        self.root.bind('<Key>', lambda event: self.key(event))

    def load_letters(self):
        self.letters = [[], [], [], [], []]
        uppers = string.ascii_uppercase
        for i in range(len(uppers)):
            if i in range(5):
                self.letters[0].append(uppers[i])
            elif i in range(5, 10):
                self.letters[1].append(uppers[i])
            elif i in range(10, 16):
                self.letters[2].append(uppers[i])
            elif i in range(16, 21):
                self.letters[3].append(uppers[i])
            else:
                self.letters[4].append(uppers[i])

    def load_strokes(self):
        self.strokes = dict()
        d = self.strokes
        d['A'] = '020312'
        d['B'] = '0102121323'
        d['C'] = '010223'
        d['D'] = '121323'
        d['E'] = '01021223'
        d['F'] = '0102'
        d['G'] = '01020323'
        d['H'] = '021213'
        d['I'] = '13'
        d['J'] = '1323'
        d['K'] = '021223'
        d['L'] = '0223'
        d['M'] = '0102031213'
        d['N'] = '020313'
        d['O'] = '01021323'
        d['P'] = '010212'
        d['Q'] = '01020312'
        d['R'] = '0212'
        d['S'] = '010323'
        d['T'] = '0113'
        d['U'] = '021323'
        d['V'] = '0313'
        d['W'] = '0203121323'
        d['X'] = '0312'
        d['Y'] = '031323'
        d['Z'] = '011223'

    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.TIMER_DELAY = 0

        self.ALL_LETTERS_SPLASH = 'all letters'
        self.SG_LETTER_SPLASH = 'single letter'
        self.TEXT_SPLASH = 'text'
        self.MARGIN = 10
        
        self.frame_count = 0

        self.splash = self.ALL_LETTERS_SPLASH
        self.important_number = 5
        self.curr_letter = None
        self.is_getting_command = False
        self.command_str = ''
        self.is_drawing_help = False
        self.is_drawing_error = False
        self.error_str = ''
        self.text_mode_text = '_'
        self.char_width = 8
        self.box_width = self.WIDTH * (self.important_number - 2) / self.important_number
        self.len_cap = int(self.box_width // self.char_width)
        self.is_drawing_letters = True
        self.is_drawing_dots = True
        self.help_txt = '''press : to enter command
Commands:
all    0    all letter mode
alpha  a    toggle alphabets
clear  c    clear all text
dots   d    toggle dots
help   h    toggle help text
text   t    enter text mode'''
        self.num_help_lines = len(self.help_txt.splitlines())

        self.load_tk()
        
        self.load_letters()
        self.load_strokes()        

    def button1(self, event): pass

    def handle_cmd_str(self):
        if self.command_str in ['help', 'h']:
            self.is_drawing_help = not self.is_drawing_help
        elif self.command_str in ['clear', 'c']:
            self.is_drawing_help = False
            self.is_drawing_error = False
        elif self.command_str in ['text', 't']:
            self.splash = self.TEXT_SPLASH
        elif self.command_str in ['alpha', 'a']:
            self.is_drawing_letters = not self.is_drawing_letters
        elif self.command_str in ['dots', 'd']:
            self.is_drawing_dots = not self.is_drawing_dots
        elif self.command_str in ['all', '0']:
            self.splash = self.ALL_LETTERS_SPLASH
        else:
            self.error_str = self.command_str
            self.is_drawing_error = True
            return
        self.is_drawing_error = False

    def key(self, event):
        if self.is_getting_command:
            if event.keysym == 'BackSpace':
                self.command_str = self.command_str[:-1]
                return
            elif event.keysym == 'Return':
                self.is_getting_command = False
                if self.command_str != '':
                    self.handle_cmd_str()
                    self.command_str = ''
                return
            else:
                self.command_str += event.char
                return
        elif self.splash == self.TEXT_SPLASH:
            if event.keysym == 'BackSpace':
                self.text_mode_text = self.text_mode_text[:-2] + '_'
                return
            elif event.keysym == 'colon':
                self.is_getting_command = True
                return
            elif event.keysym == 'Escape':
                self.splash = self.ALL_LETTERS_SPLASH
                return
            elif event.keysym == 'Return':
                self.text_mode_text = self.text_mode_text[:-1] + '\n_'
            elif event.keysym == 'space':
                self.text_mode_text = self.text_mode_text[:-1] + ' _'
            elif event.keysym.upper() in string.ascii_uppercase:
                self.text_mode_text = self.text_mode_text[:-1] + event.char + '_'
                return
        if event.keysym.upper() in string.ascii_uppercase:
            self.splash = self.SG_LETTER_SPLASH
            self.curr_letter = event.keysym.upper()
        elif event.keysym == 'Escape':
            self.splash = self.ALL_LETTERS_SPLASH
        elif event.keysym == 'colon':
            self.is_getting_command = True
        

    def timer_fired(self):
        self.frame_count += 1

        self.redraw_all()
        self.canvas.after(self.TIMER_DELAY, self.timer_fired)

    def draw4dots(self, rect):
        x0, y0, w, h = rect
        r = w / 20
        self.canvas.create_oval(x0 + w / self.important_number - r, y0 + h / self.important_number - r, x0 + w / self.important_number + r, y0 + h / self.important_number + r, fill='black', width=0)
        self.canvas.create_oval(x0 + w / self.important_number - r, y0 + h * (self.important_number - 1) / self.important_number - r, x0 + w / self.important_number + r, y0 + h * (self.important_number - 1) / self.important_number + r, fill='black', width=0)
        self.canvas.create_oval(x0 + w * (self.important_number - 1) / self.important_number - r, y0 + h * (self.important_number - 1) / self.important_number - r, x0 + w * (self.important_number - 1) / self.important_number + r, y0 + h * (self.important_number - 1) / self.important_number + r, fill='black', width=0)
        self.canvas.create_oval(x0 + w * (self.important_number - 1) / self.important_number - r, y0 + h / self.important_number - r, x0 + w * (self.important_number - 1) / self.important_number + r, y0 + h / self.important_number + r, fill='black', width=0)

    def draw_stroke(self, stroke, rect):
        x0, y0, w, h = rect
        start, end = stroke
        num = self.important_number
        cx0 = x0 + w / num + (start % 2) * w * 3 / num
        cy0 = y0 + h / num + (start > 1) * h * 3 / num
        cx1 = x0 + w / num + (end % 2) * w * 3 / num
        cy1 = y0 + h / num + (end > 1) * w * 3 / num
        r = w / 20
        self.canvas.create_line(cx0, cy0, cx1, cy1, fill='black', width=r)

    def draw_strokes(self, letter, rect):
        strokes_list = list(self.strokes[letter])
        strokes = list()
        while len(strokes_list) > 0:
            if len(strokes_list) % 2 == 0:
                strokes.append(list())
            strokes[-1].append(int(strokes_list.pop(0)))
        for stroke in strokes:
            self.draw_stroke(stroke, rect)

    def draw_letter(self, letter, rect):
        x0, y0, w, h = rect
        if self.is_drawing_letters:
            self.canvas.create_text(x0 + w / 2, y0 + h / 2, text=letter, font='Courier %d' % h, fill='#ddd')
        if self.is_drawing_dots:
            self.draw4dots(rect)
        self.draw_strokes(letter, rect)

    def draw_letters(self):
        num_rows = len(self.letters)
        vmargin = self.HEIGHT / 8
        avail_height = self.HEIGHT - 2 * vmargin
        row_height = avail_height / num_rows
        col_width = row_height
        for row_index in range(len(self.letters)):
            y0 = vmargin + row_index * row_height
            num_cols = len(self.letters[row_index])
            for col_index in range(len(self.letters[row_index])):
                x0 = self.WIDTH / 2 + col_width * (col_index - num_cols / 2)
                self.draw_letter(self.letters[row_index][col_index], (x0, y0, col_width, row_height))

    def draw_single_letter(self):
        w = h = min(self.WIDTH, self.HEIGHT)
        x0 = (self.WIDTH - w) / 2
        y0 = (self.HEIGHT - h) / 2
        self.draw_letter(self.curr_letter, (x0, y0, w, h))

    def draw_command_str(self):
        self.canvas.create_text(self.MARGIN, self.HEIGHT - self.MARGIN, text=':' + self.command_str + '_', anchor=SW, font='Courier')

    def draw_help(self):
        num_chrs = 29
        self.canvas.create_rectangle(self.WIDTH - 1.5 * self.MARGIN - self.char_width * num_chrs,
                                     self.HEIGHT - 1.5 * self.MARGIN - 13 * self.num_help_lines,
                                     self.WIDTH - self.MARGIN / 2,
                                     self.HEIGHT - self.MARGIN / 2,
                                     fill='white')
        self.canvas.create_text(self.WIDTH - self.MARGIN, self.HEIGHT - self.MARGIN, text=self.help_txt, anchor=SE, font='Courier')

    def draw_error(self):
        self.canvas.create_text(self.MARGIN, self.HEIGHT - self.MARGIN - 12, text='error: unknown command: %s' % self.error_str, anchor=SW, font='Courier', fill='red')

    def draw_text_mode_letters(self):
        x0 = y0 = self.MARGIN
        w = h = (self.WIDTH - 2 * self.MARGIN) / self.len_cap
        for char in self.text_mode_text:
            if y0 >= self.HEIGHT - h:
                return
            if char.isalpha():
                rect = (x0, y0, w, h)
                x0 += w
                if x0 >= self.WIDTH - w:
                    x0 = self.MARGIN
                    y0 += h
                self.draw_strokes(char.upper(), rect)
            elif char == '\n':
                x0 = self.MARGIN
                y0 += h
            elif char == ' ':
                x0 += w
                if x0 >= self.WIDTH - w:
                    x0 = self.MARGIN
                    y0 += h

    def draw_text_mode(self):
        aux_txt = list(self.text_mode_text)
        line_len = 0
        txt = ''
        while len(aux_txt) > 0:
            c = aux_txt.pop(0)
            txt += c
            line_len += 1
            if c == '\n':
                line_len = 0
            if line_len >= self.len_cap:
                extra = line_len - self.len_cap
                txt = txt[:(len(txt) - extra)] + '\n' + txt[(len(txt) - extra):]
                line_len -= self.len_cap
        self.canvas.create_rectangle(self.WIDTH / self.important_number, self.HEIGHT * (self.important_number - 1) / self.important_number, self.WIDTH * (self.important_number - 1) / self.important_number, self.HEIGHT - self.MARGIN)
        self.canvas.create_text(self.WIDTH / self.important_number, self.HEIGHT * (self.important_number - 1) / self.important_number, text=txt, anchor=NW, font='Courier')
        self.draw_text_mode_letters()

    def redraw_all(self):
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(0, 0, self.WIDTH, self.HEIGHT, fill='white', width=0)

        if self.splash == self.ALL_LETTERS_SPLASH:
            self.draw_letters()
        elif self.splash == self.SG_LETTER_SPLASH:
            self.draw_single_letter()
        elif self.splash == self.TEXT_SPLASH:
            self.draw_text_mode()

        if self.is_getting_command:
            self.draw_command_str()
        else:
            self.canvas.create_text(self.WIDTH - self.MARGIN, self.HEIGHT - self.MARGIN, anchor=SE, text=':h', fill='grey', font='Courier')
        if self.is_drawing_help:
            self.draw_help()
        if self.is_drawing_error:
            self.draw_error()

        self.canvas.update()

    def run(self):
        self.timer_fired()
        self.root.mainloop()

app = App()
app.run()
