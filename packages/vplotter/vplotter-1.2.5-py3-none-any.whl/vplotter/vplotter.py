from decor import deprecated
import numpy as np
import os, sys
import re

try:
    import veusz.embed as veusz
except:
    print("Veusz is not available. Aborting...")
    sys.exit(1)

try:
    from storer import Storer
except:
    print("Storer is not available. Aborting...")
    sys.exit(1)


COLOR_DICT = {
    1: 'black',     2: 'red',      3: 'green',    4: 'blue',
    5: 'magenta',   6: '#01A9DB',  7: '#006F74',  8: '#8904B1',
    9: '#B4045F',   10: '#585858', 11: '#DF3A01', 12: '#DBA901',
    13: '#74DF00',  14: '#CEF6F5', 15: '#0041FB', 16: '#00FB91',
    17: '#887D64',  18: '#00C9FF', 19: '#7625B6', 20: '#B08EA0',
}

LINE_TYPE_DICT = {
    1: 'solid',    2: 'dashed',       3: 'dotted',
    4: 'dash-dot', 5: 'dash-dot-dot', 6: 'dotted-fine', 7: 'dashed-fine', 8: 'dash-dot-fine',
    9: 'dot1',     10: 'dot2',       11: 'dot3',       12: 'dot4',
    13: 'dash1',   14: 'dash2',      15: 'dash3',      16: 'dash4',      17: 'dash5', 18: 'dash6',
}

MARKER_TYPE_DICT = {
    0: 'none',           1: 'circle',        2: 'square',         3: 'cross',       4: 'plus', 5: 'star',
    6: 'pentagon',       7: 'hexagon',       8: 'tievert',        9: 'tiehorz',    10: 'triangle',
    11: 'triangledown', 12: 'triangleleft', 13: 'triangleright', 14: 'circledot',
    15: 'bullseye',     16: 'circlehole',   17: 'squarehole',    18: 'diamondhole', 19: 'pentagonhole',
    20: 'squarerounded', 21: 'diamond',
}

# feel free to add new
LABELS_DICT = dict(
    cs= "\\italic{c}_{s}",       pK="p\\italic{K}",   pH="pH",                    lB="\\italic{l}_{B}",
    alpha="\\alpha",            chi="\\chi",           f="\\italic{f}",      epsilon="\\italic{\\epsilon}",
    sigma="\\italic{\\sigma}", dmpc="\\italic{n}", chain="\\italic{l}_{n}",    rcutg="\\italic{r}_{cut} = 2^{1/6}",
    rcut ="\\italic{r}_{cut} = 2.5",
)

def get_line_color(num):
    t = "black"
    if num <= len(COLOR_DICT) - 1 : t =  COLOR_DICT[num]
    return t

def get_line_type(num):
    t = "solid"
    if num <= len(LINE_TYPE_DICT) - 1 : t =  LINE_TYPE_DICT[num]
    return t

def get_marker_typ(num):
    t = "circle"
    if num <= len(MARKER_TYPE_DICT) - 1: t =  MARKER_TYPE_DICT[num]
    return t

def getLabel(name: str) -> str:
    return LABELS_DICT[name]

class Plotter:
    def __init__(self,
    title='NoTitle',  showkey=True, keyBorderHide=True, plotLine=True,
    xname='x', xlog=False,
    yname='y', ylog=False,
    pages_info=None,
    marker='circle',  ymin='Auto', xmin='Auto',
    markersize='2pt', ymax='Auto', xmax='Auto',
    transparency=None,):
        __version__ = "1.2.5"
        self.internal_name = "[Plotter]"
        self.storer = Storer()
        self.pages_info = pages_info
        self.xname = xname     ; self.yname = yname   ; self.plotLine = plotLine
        self.xlog = xlog       ; self.ylog = ylog     ; self.showkey = showkey       ; self.keyBorderHide = keyBorderHide
        self.title = title     ; self.marker = marker ; self.markersize = markersize
        self.ymin = ymin       ; self.xmin = xmin
        self.ymax = ymax       ; self.xmax = xmax

        if not transparency: self.transparency = 50  # default value
        else: self.transparency = transparency

        self._xy = None       # animation

        self.g = veusz.Embedded(self.title)
        self.g.EnableToolbar()

        self.init_pages()
        print(f"===> [Plotter] is initialized [v. {__version__}]")

    def _init(self, page_name=""):
        # creating initial values for plotting per page.
        self.storer.put(what="xname", name=page_name+"/xname")
        self.storer.put(what="yname", name=page_name+"/yname")
        self.storer.put(what=False,   name=page_name+"/xlog")
        self.storer.put(what=False,   name=page_name+"/ylog")
        self.storer.put(what="Auto",  name=page_name+"/xmin")
        self.storer.put(what="Auto",  name=page_name+"/xmax")
        self.storer.put(what="Auto",  name=page_name+"/ymin")
        self.storer.put(what="Auto",  name=page_name+"/ymax")

    def init_pages(self):
        if self.pages_info:
                for page in self.pages_info:
                    self._init(page_name=page)
                    for prop in self.pages_info[page]:
                        self.storer.put(what=self.pages_info[page][prop] , name=page+"/"+prop)
        else:
            self._init(page_name="page1")
            self.storer.put(what=self.xname , name="page1/xname")
            self.storer.put(what=self.yname , name="page1/yname")

            self.storer.put(what=self.xlog  , name="page1/xlog")
            self.storer.put(what=self.ylog  , name="page1/ylog")

            self.storer.put(what=self.xmin  , name="page1/xmin")
            self.storer.put(what=self.xmax  , name="page1/xmax")

            self.storer.put(what=self.ymax  , name="page1/ymax")
            self.storer.put(what=self.ymin  , name="page1/ymin")


    def get_page(self, name="page1"):

        try:
            self.page = self.g.Root[name]
            _num_lines  = self.storer.get(name=name+ "/_num_lines")
            __num_lines = self.storer.get(name=name+"/__num_lines")  # if save_previous_state is applied
        except KeyError:
            self.page = self.g.Root.Add("page")
            self.page.Rename(name)
            __num_lines = 1; _num_lines = 1
            self.storer.put(what=_num_lines, name=name+ "/_num_lines")
            self.storer.put(what=__num_lines, name=name+ "/__num_lines")

        self.page.width.val = '15cm'
        self.page.height.val = '10cm'

        try: self.graph = self.g.Root[name + '/graph1']
        except: self.graph = self.page.Add('graph')

        try:
            # key exist
            self.key = self.g.Root[name + "/graph1/key1"]
        except:
            if self.showkey:
                self.graph.Add('key')
                self.graph.key1.Border.hide.val = self.keyBorderHide

        return _num_lines, __num_lines


    def name_converter(self: object, name: str) -> str:
        if name.find(" ") != -1: print("Please, use notation: `varX_var2Y.YY_var3ZZ.Z`")
        name = name.replace(" ", "").replace("=","")

        res = []
        parts = name.split("_")

        for part in parts:
            if part[0:4] == "time": res.append(part); continue
            m = re.search(r"[+-]?[\d.]*\d+", part)
            if m:
                try: symbol = getLabel(part[:m.start()])
                except KeyError: symbol = part[:m.start()]
                #part_ = symbol + "_{" + m.string[m.start():m.end()] + "}"
                part_ = symbol + " = " + m.string[m.start():m.end()]
            else:
                #part_ = part
                try: part_ = getLabel(part)
                except KeyError: part_ = part
            res.append(part_)

        return " ".join(res)

    def plot(self, x, y, key_name_f='', key_name="",
             marker_type="auto", markersize='2.5pt',
             plotLine=True, color_num='auto', line_type='auto',
             save_previous_state=False, animation=False, errorStyle = None,
             internal_text = "", page="page1", move_up_curve = False, move_down_curve = False,
             ):

        _num_lines, __num_lines = self.get_page(name=page)

        if animation:
            color_num = _num_lines
            line_type = _num_lines
            save_previous_state = True
            xy = self._xy

        if save_previous_state: _num_lines -= 1

        if color_num == "auto": color_num = _num_lines
        if line_type == "auto": line_type = _num_lines

        if not animation:
            x_dataname = self.xname + str(_num_lines) + str(save_previous_state) + str(__num_lines) + str(page)
            y_dataname = self.yname + str(_num_lines) + str(save_previous_state) + str(__num_lines) + str(page)
        else:
            x_dataname = self.xname + str(_num_lines) + str(save_previous_state) + str(page)
            y_dataname = self.yname + str(_num_lines) + str(save_previous_state) + str(page)

        x_dataname += internal_text
        y_dataname += internal_text

        # TODO: too weak
        if len(np.shape(x)) == 2:
            x_data, x_data_err = x[0], x[1]
            self.g.SetData(x_dataname, x_data, symerr=x_data_err)
        else:
            x_data = x
            self.g.SetData(x_dataname, x_data)
        if len(np.shape(y)) == 2:
            y_data, y_data_err = y[0], y[1]
            self.g.SetData(y_dataname, y_data, symerr=y_data_err)
        else:
            y_data = y
            self.g.SetData(y_dataname, y_data)

        # self.graph = self.g.Root[name + '/graph1']
        if animation:
            if not self._xy: self._xy = xy = self.g.Root[page + '/graph1'].Add('xy')
        else: xy = self.g.Root[page + '/graph1'].Add('xy')

        # nn.plotter_progress.g.Root.xyz_file.graph1.xy1.Clone(nn.plotter_progress.g.Root.xyz_file.graph1, 'xy7')
        xy.xData.val = x_dataname
        xy.yData.val = y_dataname
        if marker_type != "auto": xy.marker.val = get_marker_typ(marker_type)
        else: xy.marker.val = get_marker_typ(line_type)

        if color_num % 2: xy.MarkerFill.color.val = get_line_color(color_num)
        else: xy.MarkerFill.color.val = 'white'

        xy.MarkerLine.color.val = get_line_color(color_num)
        xy.markerSize.val     = markersize
        xy.PlotLine.width.val = '1pt'
        xy.PlotLine.style.val = get_line_type(line_type)
        xy.PlotLine.color.val = get_line_color(color_num)
        xy.PlotLine.hide.val  = not plotLine

        if errorStyle:
            xy.errorStyle.val             = errorStyle
            xy.FillBelow.color.val        = get_line_color(color_num)
            xy.FillBelow.transparency.val = self.transparency
            xy.FillAbove.color.val        = get_line_color(color_num)
            xy.FillAbove.transparency.val = self.transparency

            #ErrorBarLine/style
            xy.ErrorBarLine.color.val = get_line_type(line_type)
            xy.ErrorBarLine.style.val = get_line_type(line_type)
        else:
            xy.errorStyle.val = 'none'

        xy.ErrorBarLine.width.val = '1pt'
        xy.ErrorBarLine.color.val = get_line_color(color_num)
        if self.showkey and key_name_f: xy.key.val = self.name_converter(key_name_f)
        if self.showkey and key_name: xy.key.val = key_name

        x_axis = self.graph.x
        y_axis = self.graph.y

        x_axis.label.val = self.storer.get(page+"/xname") # self.xname
        y_axis.label.val = self.storer.get(page+"/yname") # self.yname

        x_axis.log.val = self.storer.get(page+"/xlog") # self.xlog
        y_axis.log.val = self.storer.get(page+"/ylog") # self.ylog

        x_axis.min.val = self.storer.get(page+"/xmin") # self.xmin
        x_axis.max.val = self.storer.get(page+"/xmax") # self.xmax

        y_axis.min.val = self.storer.get(page+"/ymin") # self.ymin
        y_axis.max.val = self.storer.get(page+"/ymax") # self.ymax

        _num_lines  += 1
        __num_lines += 1
        self.storer.put(_num_lines, name=page+ "/_num_lines")
        self.storer.put(__num_lines, name=page+ "/__num_lines")

    @deprecated
    def make_label(self,  chi=0, N=0, sigma=0, a=0):
        label = self.graph.Add('label')
        label.label.val += '\\\\\\chi = ' + str(chi) + '\\\\ \sigma = ' + str(sigma) + '\\\\N = ' + str(N) + ', a = ' + str(a)
        # label.label.val += '\\\\\\chi = ' + str(chi) + ', pH = ' + str(pH) + '\\\\c_{s} = ' + '{:.2e}'.format(cs) + ' mol/l'
        label.xPos.val = 0.65
        label.yPos.val = 0.75

    @deprecated
    def make_smallabel(self, t = 0, color_num = 1):
        label2 = self.graph.Add('label')
        label2.label.val = 't = ' + str(t)
        label2.xPos.val = 0.6
        label2.yPos.val = 0.4
        label2.Text.color.val = get_line_color(color_num)

    def export(self, filename=None, extension=None, color=True, page=0, dpi=100, antialias=True, quality=85, backcolor='#ffffff00', pdfdpi=150, svgtextastext=False):
        if not filename or not extension:
            print(f"{self.internal_name} You have to specify filename and extension!")
            print(f"{self.internal_name} For example: my_amazing_figure")
            print(f"{self.internal_name} Available extensions: [pdf]/[eps]/[ps]/[svg]/[jpg]/[jpeg]/[bmp]/[png]]")
        else: self.g.Export(filename, color=color, page=page, dpi=dpi, antialias=antialias, quality=quality, backcolor=backcolor, pdfdpi=pdfdpi, svgtextastext=svgtextastext)

    def save(self, filename=None):
        if not filename:
            print(f"{self.internal_name} You have to specify filename! [Labels from Y and X will be added automatically]")
        else:
            if filename.find(".") != -1 or filename.find(":") or filename.find("\\") or filename.find("*") or filename.find("/") or filename.find("\\\\"):
                print(f"{self.internal_name} I found forbidden symbols [.]/[:]...")
                filename.replace(".", "").replace(":", "_").replace("\\\\","").replace("*", "").replace("/", "_").replace("\\", "")

            # latex reduction
            xname = self.xname.replace("\\italic", "").replace("{", "").replace("}","").replace("_", "").replace("^", "").replace("\\\\", "").replace("\\", "").replace("/", "_").replace("*", "")
            yname = self.yname.replace("\\italic", "").replace("{", "").replace("}","").replace("_", "").replace("^", "").replace("\\\\", "").replace("\\", "").replace("/", "_").replace("*", "")
            # space reduction
            xname = xname.replace(" ", "")
            yname = yname.replace(" ", "")

            name4saving = filename+"_"+yname+"_"+xname

            if not os.path.exists(name4saving+".vsz"): self.g.Save(name4saving+".vsz")
            else:
                print(f"{self.internal_name} The file exists!")
                i = 0
                while os.path.exists(name4saving+str(i)+".vsz"): i+=1
                name4saving += str(i) + ".vsz"
                self.g.Save(name4saving)
                print(f"{self.internal_name} Saved! filename: {name4saving}")

# Testing properties
if __name__ == "__main__":
    p = Plotter(
        pages_info={
            "page1" : {
                "xname" : "page1_x",  "yname" : "page1_y",
                "xlog"  : False, "ylog" : False,
                "ymin" : "Auto", "ymax" : "Auto",
                "xmin" : "Auto", "xmax" : "Auto",
                },
           "page2" :{
                "xname" : "page2_x",  "yname" : "page2_y",
                "xlog"  : True, "ylog" : True,
                }
        }
    )

    p.plot(x=[1,1,2], y=[1,2,3], key_name="first", page="page1")
    p.plot(x=[0,0,6], y=[1,2,3], key_name="second", page="page1")

    p.plot(x=[i**2 for i in range(10)], y=[i**3 for i in range(10)], key_name="first", page="page2")
    p.plot(x=[1,3,7], y=[6,2,2], key_name="second", page="page2")

    p_one_page = Plotter(xname="A", yname="B", xlog=True, ylog=False, )
    p_one_page.plot(x=[i for i in range(100)], y=[j for j in range(100)], key_name_f="MyName")
    p_one_page.plot(x=[i for i in range(100)], y=[j for j in range(100)], key_name_f="MyName1")
    p_one_page.plot(x=[i for i in range(100)], y=[j for j in range(100)], key_name="MyName1")
