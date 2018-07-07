import os
import sys
import json
import uuid
import random

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ui import style

import airtable
import datetime
import astral






AIRTABLE_API_KEY = 'keyyeOyrgbQQ9qvLh'
os.environ['AIRTABLE_API_KEY'] = AIRTABLE_API_KEY


#PLAN
#PLAN
"""
Create a main window that houses the different aspect widgets. 
These aspect widgets will be little helpers for various agendas throughout a workday. These will evolve over time. Because of this, first begin developing the framework
of how your main session can be aware of what is 'attention needed' in any given widget, and setup a window framework that each widget can inherit. 

"""
class Engine(QWidget):
    def __init__(self):
        super(Engine, self).__init__()
        pass

class ElidedLabel(QLabel):

    def paintEvent(self, event):
        painter = QPainter(self)
        metrics = QFontMetrics(self.font())
        elided = metrics.elidedText(self.text(), Qt.ElideRight, self.width())
        painter.drawText(self.rect(), self.alignment(), elided)

class UlyssesItem(QWidget):
    def __init__(self):
        super(UlyssesItem, self).__init__()

        self.title = QLabel("Title")
        self.font = QFont()
        self.font.setBold(True)
        self.title.setFont( self.font )

        self.time = QLabel(datetime.datetime.now().strftime( "%A %m/%d/%y %I:%M %p"))
        timefont = QFont()
        timefont.setPointSize( 9 )
        self.time.setFont( timefont )

        self.master_layout = QVBoxLayout()
        self.master_layout.setContentsMargins(2,2,2,2)
        self.master_layout.setSpacing( 2 )

        self.txt = QLabel()
        self.txt.setText("this sdfsdfsdf"
                     "sdfsfsdfsdfsdf"
                     "is an example document that donald had written he said lorem ipsum something, "
                     "something or something else.")
        self.txt.setWordWrap(True)
        self.master_layout.addWidget( self.time )
        self.master_layout.addWidget( self.title )
        self.master_layout.addWidget(self.txt)
        self.master_layout.addStretch(1)
        self.setLayout( self.master_layout )



class Silo(QWidget):
    '''
    Silos are the QWidget frames that inherit the main engine. Each one contains its own tasks, dates, etc for looku by the engine.


    '''

    new_notification = Signal(str)


    def __init__(self):
        super(Silo, self).__init__()
        self.master_layout = QVBoxLayout()


        self._master_layout_ = QVBoxLayout()
        self._master_layout_.setContentsMargins( 0,0,0,0 )
        self.setLayout( self._master_layout_ )

        #ENGINE DATA ARCHETYPES
        self.dates = {}
        self.tasks = {}

        self.base = {}
        self.model = {}

        self.top_button_bar = QToolBar()
        self._master_layout_.addWidget(self.top_button_bar)
        self._master_layout_.addLayout( self.master_layout )
        self.top_button_bar.setVisible(False)

        self.emoji_util = EmojiUtils()


    def new_airtable_connection(self, key, base_name):
        """
        Will establish connection and retrieve table from Airtable. Adds to collection
        :param key:
        :param base_name:
        :return:
        """
        self.base[base_name] = airtable.Airtable(key, base_name)
        self.model[base_name] = self.base[base_name].get_all()


####TODO:: Ulysses is now charging. I just paid 50 last year for it, now they want subscription.
####TODO:: Write Ulysses alternative

class EugeneRoe(Silo):
    def __init__(self):
        super(EugeneRoe, self).__init__()


        self.base = "/Users/donaldstrubler/Documents/WRITE"
        self.projects = os.walk( self.base )

        self.splitter = QSplitter(Qt.Horizontal)

        self.project_tree = QTreeWidget()
        header = QTreeWidgetItem(["Project"])
        # ...
        self.project_tree.setHeaderItem(header)  # Another alternative is setHeaderLabels(["Tree","First",...])

        self.root = QTreeWidgetItem(self.project_tree, ["Blogging"])
        self.set_icon( self.root, 'notebook-3' )
        self.root.setBackground( 0, QBrush( QColor( 60, 60, 60, 200 ) ) )
        self.root.setSizeHint( 0, QSize(0, 30))
        A = QTreeWidgetItem(self.root, ["A"])

        bazA = QTreeWidgetItem(A, ["baz"])

        root2 = QTreeWidgetItem(self.project_tree, ["Cloud"])
        #root2.setSizeHint(0, QSize(0, 30))
        A2 = QTreeWidgetItem(root2, ["iCloud"])
        self.barA2 = QTreeWidgetItem(A2, ["bar"])
        self.set_icon( self.barA2, 'map-location' )

        bazA2 = QTreeWidgetItem(A2, ["baz"])

        A2.setIcon( 0, QIcon( QPixmap( "/Users/donaldstrubler/PycharmProjects/MysteryMachine/ui/icons/white/cloud-computing-2.png" ) ) )

        self.items_list = QListWidget()
        self.write = QPlainTextEdit()

        document =  self.write.document()

        font = document.defaultFont()
        font.setFamily("Courier New")
        document.setDefaultFont(font)

        self.project_tree.setIconSize(QSize(18,18))


        treepalette = self.project_tree.palette()


        treepalette.setColor(QPalette.Highlight, QColor(70, 70, 70, 215))
        self.project_tree.setPalette( treepalette )


        cl =  UlyssesItem()


        self.project_tree.setIndentation( 15 )
        self.project_tree.header().hide()

        self.splitter.addWidget( self.project_tree )
        self.splitter.addWidget( self.items_list )
        self.splitter.addWidget( self.write )

        self.master_layout.addWidget( self.splitter )

        self.items = {}
        self.docs = {}
        for i in range(10):
            self.items[i] = QListWidgetItem()
            self.items[i].setSizeHint(QSize(0, 90))
            self.items_list.addItem( self.items[i] )
            self.docs[i] = UlyssesItem()
            self.items_list.setItemWidget( self.items[i] , self.docs[i]  )


        self.project_tree.expandToDepth(10)
        self.project_tree.setAnimated(True)

    def set_icon(self, item, icon):
        item.setIcon(0, QIcon( QPixmap("/Users/donaldstrubler/PycharmProjects/MysteryMachine/ui/icons/white/%s.png" %icon)))

class Tasks(Silo):
    def __init__(self):
        super(Tasks, self).__init__()

        self.schedule = QTableWidget()
        self.master_layout.addWidget( self.schedule )

        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        #self.schedule.setRowCount( len( days ) )
        c = 0
        self.schedule.setColumnCount(1)
        for day in days:
            self.schedule.insertRow( c )
            d = QTableWidgetItem( day )
            self.schedule.setItem( c, 0 , d)
            c+=1

class Puja(Silo):
    def __init__(self):
        super(Puja, self).__init__()
        self.top_button_bar.setVisible(True)
        self.act = QAction( 'Puja' )
        self.top_button_bar.addAction( self.act )
        pass


class QuoteMaker(Silo):
    '''
    TODO
    '''
    def __init__(self):
        super(QuoteMaker, self).__init__()

        self.label = QToolButton(  )
        self.label.setText( 'QuoteMaker' )

        self.top_bar = QHBoxLayout()
        self.add_quote = QToolButton()
        self.add_quote.setText('+ Quote')
        self.top_bar.addWidget( self.add_quote )
        self.top_bar.addStretch(1)
        self.master_layout.addLayout( self.top_bar)


        self.schedule = QTableWidget()
        self.master_layout.addWidget( self.schedule )



        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        #self.schedule.setRowCount( len( days ) )
        c = 0
        self.schedule.setColumnCount(1)
        for day in days:
            self.schedule.insertRow( c )
            d = QTableWidgetItem( day )
            self.schedule.setItem( c, 0 , d)
            c+=1

        #airtable
        #self.new_airtable_connection('appJLatmhJPKftvrd', 'Quotes')
        #print self.model


class EmojiUtils(object):
    def __init__(self):
        super(EmojiUtils, self).__init__()

        self.base = "/Users/donaldstrubler/PycharmProjects/nukemoji"
        self.eac_json = "%s/eac.json" % self.base
        self.map = {}
        self.load_eac_json()

    def load_eac_json(self):
        with open(self.eac_json) as f:
            data = json.load(f)
            emoji_exists = [p.replace('.png', '') for p in os.listdir("%s/lib_128works" % self.base)]
            self.map = dict((str(v['alpha_code']), str(v['output'])) for k, v in data.iteritems() if
                            str(v['output']) in emoji_exists)

    def get_path_from_keyword(self, word):
        return "%s/lib_128works/%s.png" %(self.base, self.map[":%s:" %word])

class EventButton(QToolButton):

    event_checked = Signal(object)

    def __init__(self, parent, name):
        super(EventButton, self).__init__()
        self.parent = parent
        self.hour = 0
        self.font = QFont()
        self.font.setCapitalization( QFont.AllUppercase )
        self.id = "%s.%s" %(name, str(uuid.uuid4()))

        self.font.setPixelSize( 11 )
        self.font.setLetterSpacing( QFont.AbsoluteSpacing, 1.1 )




        self.menu = QMenu()
        self.emoji_act = QAction( self.menu )
        self.emoji_act.setText('change emoji')

        self.setMenu( self.menu )

        self.bottom_menu = QToolBar()
        self.t1 = QAction(self.bottom_menu)
        self.t1.setText( "DONE" )
        self.t2 = QAction(self.bottom_menu)
        self.t2.setText( "START" )
        for t in [self.t1, self.t2]:
            self.bottom_menu.addAction(t)

        self.wAction = QWidgetAction(self)
        self.sd = ShirtDesigner()
        self.wAction.setDefaultWidget(self.bottom_menu)
        self.menu.addAction(self.wAction)
        self.menu.addAction( self.emoji_act )

        self.setPopupMode( QToolButton.MenuButtonPopup )

        toolbuttonSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setSizePolicy(toolbuttonSizePolicy)
        #meta # self.items[name] = QToolButton()
        self.setMinimumHeight(30)
        self.setFont( self.font )
        self.setAutoRaise(True)

        self.setCheckable(True)
        self.setAutoFillBackground(True)
        self.setStyleSheet( "background-color:rgba(85,90,100,100);" )
        if 'tgm' in name.lower():
            self.setStyleSheet("background-color:rgba(140,85,30,180);")
        if name.lower()=="sleep":
            self.setStyleSheet("background-color:rgba(50,60,80,90);")
        self.setText(name)
        self.set_emoji("kissing_cat")

        self.clicked.connect( self.send_self )

    def set_hour(self, hour):
        self.hour = hour

    def send_self(self):

        self.event_checked.emit(self)

    def make_small(self):
        toolbuttonSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setSizePolicy(toolbuttonSizePolicy)

    def set_emoji(self, emoji=None):


        path = self.parent.emoji_util.get_path_from_keyword(random.choice( self.parent.emoji_util.map.keys() ).replace(":", ""))
        pxm = QPixmap(path)
        pxm.scaledToHeight(24, Qt.SmoothTransformation)
        icon = QIcon(pxm)
        self.setIcon( icon )
        self.setIconSize(QSize(24, 24))
        self.setToolButtonStyle( Qt.ToolButtonTextBesideIcon )

        palette = self.palette()


        palette.setBrush(self.backgroundRole(), QBrush(pxm));

        self.setPalette(palette)




        #set icon to emoji. This will be a standard used setting in subclasses



class AgendaItem(QWidget):

    hourDoubleClicked = Signal( object )
    cellSelected = Signal(int)

    def __init__(self, parent, hour):
        super(AgendaItem, self).__init__()

        self.master_layout = QHBoxLayout()
        self.items = {}
        self.hour = hour
        self.parent = parent

        self.loaded_hour = False


        self.master_layout.setContentsMargins( 10,0,3,0 )
        self.master_layout.setSpacing(6)


        self.setMinimumHeight( 40 )
        self.setMinimumWidth( 200 )

        self.setLayout( self.master_layout )

    def mousePressEvent(self, event):

        self.last = "Click"

    def mouseReleaseEvent(self, event):

        if self.last == "Click":
            self.cellSelected.emit(self.hour)
            QTimer.singleShot(QApplication.instance().doubleClickInterval(),
                              self.performSingleClickAction)
        else:
            self.hourDoubleClicked.emit( self )
            self.message = "Double Click"
            self.update()

    def mouseDoubleClickEvent(self, event):

        self.last = "Double Click"

    def performSingleClickAction(self):

        if self.last == "Click":

            self.update()

    def add_item_input(self):
        task_name, ok = QInputDialog.getText(self, 'Name Your Shirt', 'name:')
        if ok:
            self.add_item( task_name )


    def add_item(self, name, event=None):
        #TODO:: make own class. Really needs to be a base level Event class, and then special "Apps" can make their own event interface, to preview the workflow.
        index = len(self.items.keys())
        if event:
            self.items[event.text()] = event
            self.items[event.text()].set_hour( self.hour )
            print "%s = %s" %(self.items[event.text()].text(),self.items[event.text()].hour )
            self.master_layout.insertWidget(0, self.items[event.text()])
        else:
            font = QFont()
            font.setCapitalization( QFont.AllUppercase )

            font.setPixelSize( 11 )
            font.setLetterSpacing( QFont.AbsoluteSpacing, 1.1 )


            self.items[name] = EventButton(self, name)
            self.items[name].set_hour( self.hour )

            self.master_layout.insertWidget( 0  , self.items[name])

    def pop_item(self, event):
        #self.master_layout.removeWidget(event)
        del self.items[event.text()]


class DayPlanner(Silo):
    def __init__(self):
        super(DayPlanner, self).__init__()

        self.events = {}
        now = datetime.datetime.now()
        self.day = ( now.year, now.month, now.day )
        self.top_button_bar.setVisible(True)
        self.act = QAction( 'new day' )
        self.top_button_bar.addAction( self.act )

        self.stn = QAction('scroll to now')
        self.top_button_bar.addAction(self.stn)

        self.down = QAction('down')
        self.top_button_bar.addAction(self.down)
        self.up = QAction('up')
        self.top_button_bar.addAction(self.up)

        self.small = QAction('small')
        self.top_button_bar.addAction(self.small)

        self.done = QAction('done')
        self.top_button_bar.addAction(self.done)

        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        now = datetime.datetime.now()
        self.date.setDate( QDate( now.year, now.month, now.day ) )
        self.master_layout.addWidget( self.date )



        self.act.triggered.connect( self.add_event )
        self.stn.triggered.connect( self.scroll_to_now )
        self.up.triggered.connect(self.move_events_up )
        self.down.triggered.connect(self.move_events_down)
        self.small.triggered.connect(self.make_small)
        self.done.triggered.connect( self.what_day)

        self.schedule = QTableWidget()
        self.master_layout.addWidget( self.schedule )

        self.agenda = {}

        self.planner = {}
        self.planner[ now.strftime("%Y%m%d") ] = {}


        #self.populateDay()


        self.schedule.horizontalHeader().setStretchLastSection(True)

        self.sched_pal = self.schedule.palette()
        self.sched_pal.setColor(QPalette.Highlight, QColor(120, 120, 120, 15))
        self.schedule.setPalette( self.sched_pal )
        self.schedule.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.date.dateChanged.connect( self.add_events_from_log )

        #self.add_events_from_log()


    def set_day(self, day):
        pass


    def what_day(self):
        print self.day

    def strday(self):
        print "%04d%02d%02d" %( self.day[0], self.day[1], self.day[2] )

    def complete(self):
        for i, e in self.events.iteritems():

            if e.isChecked():
                e.setVisible(False)




    def string_in(self, string):
        """
        Sees if string is already in row.
        :param string:
        :return:
        """


    def add_event(self, hour, string=None):
        if string:
            task_name = string
            ok = True
        else:
            task_name, ok = QInputDialog.getText(self, 'Task', 'name:')
            hour = hour.hour
        if ok:

            name = task_name
            event =  EventButton(self, name)
            name = event.id
            self.events[name] = event
            self.events[name].set_hour( hour )
            self.events[name].event_checked.connect( self.register_selection_choice )

            self.agenda[hour].master_layout.insertWidget( 0 , self.events[name])
            self.write_day_log()

    def serialize_day(self):
        day = {}
        for h, v in self.agenda.iteritems():

            cn =  v.master_layout.count()
            hr = []
            if cn>0:
                day[h] = hr
                for w in range(cn):
                        day[h].append( v.master_layout.itemAt(w).widget().text() )
        return day

    def write_day_log(self):
        day = str(self.day[0])+str(self.day[1])+str(self.day[2])
        base = "/Users/donaldstrubler/Documents/MysteryMachine/DayPlanner"
        fl = "%s/%s.log" %( base, day )
        with open(fl, 'w') as outfile:
            json.dump(self.serialize_day(), outfile)

    def change_day(self):
        #self.schedule.clear()
        day = self.date.date()
        self.date = (day.year, day.month, day.day)
        print self.date
        #self.add_events_from_log()



    def move_event(self, offset):
        for i,e in self.events.iteritems():
            if e.isChecked():
                ind = e.hour
                if -1<(ind+offset)<24:
                    self.agenda[ind].master_layout.removeWidget(e)
                    e.set_hour( ind+offset )


                    self.agenda[ind+offset].master_layout.insertWidget(0, e)
                    #self.agenda[ind+offset].master_layout.setStretchFactor( e, 1 )

        self.write_day_log()


    def make_small(self):
        for i,e in self.events.iteritems():
            if e.isChecked():
                e.make_small()

    def register_selection_choice(self, button, clear=None):
        shift = None
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            shift=True
        if not shift:
            for i,e in self.events.iteritems():

                if e.isChecked():


                    e.setChecked(False)
            if clear==None:

                if button.isChecked():

                    button.setChecked(False)
                else:
                    button.setChecked(True)



    def move_events_up(self):
        self.move_event(-1)

    def move_events_down(self):
        self.move_event(1)

    def move_events(self, dir):
        mv_ls = []
        if dir is not 0:
            for i,v in self.agenda.iteritems():
                c = v.hour
                for k,e in v.items.iteritems():

                    if e.isChecked():

                        mv_ls.append(e)
                        print e.text()
            for ev in mv_ls:
                if ev.hour+dir<24 and ev.hour-dir>-2:
                    self.agenda[ev.hour+dir].add_item(None, event=ev)
                    self.agenda[ev.hour].pop_item(ev)



    def populateDay(self):
        self.schedule.clear()
        hours = list(xrange(1,25))
        print "%s hour objs" %len(hours)
        #self.schedule.setRowCount( len( days ) )
        c = 0
        hrz = [12]+(list(xrange(1,13))*2)[:-1]
        hour_readable = [ "%s AM" %str(q) if i < 12 else "%s PM" %str(q) for i,q in enumerate(hrz) ]
        self.schedule.setColumnCount(3)
        self.schedule.verticalHeader().hide()

        self.schedule.setHorizontalHeaderLabels(['Time', 'tbd', 'Agenda'])
        self.schedule.horizontalHeaderItem( 0 ).setTextAlignment(Qt.AlignHCenter)

        night = QColor(205,220,255,170)
        morning = QColor(255, 245, 130, 180)
        afternoon = QColor(255, 165, 90, 160)
        evening = QColor(210, 150, 180, 190)

        for hour in hours:

            self.schedule.insertRow( c )

            t = QTableWidgetItem( hour_readable[c] )


            t.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            t.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            font = QFont()
            font.setPointSize(10)
            font.setBold(False)



            self.agenda[c] = AgendaItem(self, c)
            self.agenda[c].hourDoubleClicked.connect( self.add_event )
            self.agenda[c].cellSelected.connect(self.select_row)
            self.schedule.setCellWidget(c, 2, self.agenda[c])

            #s.setMinimumHeight(30)
            if c<6:
                t.setForeground( QBrush(night) )
            if c==6:
                t.setForeground( QBrush( self.mix_colors( night, morning, (0.7,0.3 )  ) ))
            if c>6 and c<15:
                t.setForeground(QBrush(morning))
            if c==15:
                t.setForeground(QBrush(self.mix_colors(morning, afternoon, (0.5, 0.5))))
            if c>15 and c<19:
                t.setForeground(QBrush(afternoon))
            if c == 19:
                t.setForeground(QBrush(self.mix_colors(afternoon, evening, (0.5, 0.5))))
            if c>19:
                t.setForeground(QBrush(evening))
            if c==23:
                t.setForeground(QBrush(self.mix_colors(night, evening, (0.5, 0.5))))
            t.setBackground(QBrush(QColor(60, 60, 60, 80)))
            t.setFont(font)

            #if weekend day:
            if datetime.datetime.now().strftime( "%w" ) in [0,6]:
                if (c>8 and c<19):
                    t.setBackground( QBrush( QColor( 100,100,100,55 ) )  )
            #set the item.

            self.schedule.setItem( c, 0 , t)
            c+=1
        self.schedule.setColumnWidth(0,45)
        self.schedule.setColumnWidth(1, 35)
        self.schedule.resizeRowsToContents()
        self.schedule.resizeColumnToContents(2)
        #self.scroll_to_now()

    def select_row(self, row):
        self.register_selection_choice(None, clear=True)
        self.schedule.selectRow(row)

    def mix_colors(self, color1, color2, mix):
        return QColor(mix[0] * color1.red() + mix[1]* color2.red(),
                      mix[0] * color1.green() + mix[1] * color2.green(),
                      mix[0] * color1.blue() + mix[1] * color2.blue(),
                      mix[0] * color1.alpha() + mix[1] * color2.alpha())

    def add_events_from_log(self):
        try:
            self.populateDay()
            day = str(self.day[0])+str(self.day[1])+str(self.day[2])
            base = "/Users/donaldstrubler/Documents/MysteryMachine/DayPlanner"
            fl = "%s/%s.log" %( base, day )
            with open(fl) as f:
                data = json.load(f)
            for k,v in data.iteritems():
                for i in v:

                    self.add_event( int(k), i )
        except:
            pass

    def scroll_to_now(self):
        now = datetime.datetime.now()
        now_str = now.strftime("%-I %p")
        items = self.schedule.findItems( now_str, Qt.MatchExactly)
        if items:
            self.schedule.scrollToItem( items[0], QAbstractItemView.PositionAtTop )
            items[0].setBackground(QBrush(QColor(100, 100, 100, 120)))
            items[0].setForeground(QBrush(QColor(250, 250, 250, 240)))
            font = QFont()
            font.setPointSize(10)
            font.setBold(True)
            items[0].setFont(font)


class ShirtDesigner(Silo):
    def __init__(self):
        super(ShirtDesigner, self).__init__()
        #maybe register all things here, calendar, etc.

        self.base = "/Users/donaldstrubler/Documents/CREATE/TSHIRTS"
        self.project_list = QListWidget()


        self.top_button_bar.setVisible(True)
        self.act = QAction( 'new shirt' )
        self.act.triggered.connect( self.make_new_project )
        self.top_button_bar.addAction( self.act )
        self.master_layout.addWidget( self.project_list )

        self.refresh_project_list()


    def get_projects(self):
        return sorted([i for i in os.listdir( self.base ) if not i.startswith('_') and i not in ['.DS_Store']])

    def get_next_index(self):
        return int(self.get_projects()[-1].split('_')[0])+1

    def refresh_project_list(self):
        self.project_list.clear()
        self.project_list.addItems( self.get_projects() )

    def make_project(self, name):
        project = "%03d_%s" %( self.get_next_index(), name.upper() )
        path = "%s/%s" %( self.base , project)
        os.makedirs(path)
        self.refresh_project_list()

    def make_new_project(self):
        text, ok = QInputDialog.getText(self, 'Name Your Shirt', 'name:')
        if ok:
            name = str(text)
            self.make_project(name)



class BirthdayBoy(Silo):
    #widget to display the next 4 birthdays coming up, and auto looks for gifts.
    def __init__(self):
        super(BirthdayBoy, self).__init__()
        #maybe register all things here, calendar, etc.
        pass

    def __init__(self):
        super(BirthdayBoy, self).__init__()

        self.master_layout = QVBoxLayout()
        self.birthday_table = QTableWidget()

class BloodBank(Silo):
    def __init__(self):
        super(BloodBank, self).__init__()
        #WRiTING APP


class Panel(QWidget):
    def __init__(self):
        super(Panel, self).__init__()
        self.setWindowTitle('TheeMysteryMachine')
        self.master_layout = QVBoxLayout()
        self.setLayout( self.master_layout )
        self.label = QPushButton( 'MysteryMachine' )

        self.setMinimumWidth( 900 )
        self.setMinimumHeight(900)
        #self.master_layout.addWidget( self.label )

        self.tabs = QTabWidget()
        self.tab = {}
        self.tab['QuoteMaker'] = QuoteMaker()
        self.tab['DayPlanner'] = DayPlanner()
        self.tab['ShirtDesigner'] = ShirtDesigner()

        self.tabs.addTab( self.tab['DayPlanner'], 'DayPlanner' )
        self.tabs.addTab( self.tab['QuoteMaker'], 'QuoteMaker' )




        self.tasks = Tasks()

        self.puja = Puja()
        self.eugene = EugeneRoe()
        self.side_splitter = QSplitter(Qt.Vertical)
        self.side_splitter.addWidget(   self.puja )
        self.side_splitter.addWidget( self.eugene )
        self.side_splitter.addWidget( self.tab['ShirtDesigner'] )




        self.splitter_B = QSplitter(Qt.Horizontal)
        self.splitter_B.addWidget( self.tabs )
        self.splitter_B.addWidget( self.side_splitter)


        self.event_viewer = QStackedWidget()
        self.events = {}



        self.master_layout.addWidget(self.splitter_B)









if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    style.dark(app)
    window = Panel()
    window.show()
    sys.exit(app.exec_())

