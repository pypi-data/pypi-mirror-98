import sys
import os
from typing import Callable, Dict
import time
import traceback
import contextvars
from PySide2.QtWidgets import QApplication, QDialog, QPushButton, QWidget, QGridLayout, QStyle, QLabel, QDoubleSpinBox, QGroupBox, QComboBox
from PySide2.QtCore import QSize, Qt, QRectF, QTimer, SLOT
from PySide2.QtGui import QPainter, QColor
from simanim.abstract.core import AnimContext, AnimVars, InputFloat, InputList
from .driver import DrawingDriverQt

class AnimRenderArea(QWidget):

    def __init__(self, parent, anim_context: AnimContext): # a string literals for a forward type rererence
        super().__init__(parent)
        self.anim_context = anim_context
        self.setAutoFillBackground(False) # we will fill background on each paint event
        self.paint_error_occurred = False

    def sizeHint(self):
        return QSize(self.anim_context.settings.window_with_px, self.anim_context.settings.window_height_px)
    
    def minimumSizeHint(self):
        return QSize(self.anim_context.settings.window_with_px, self.anim_context.settings.window_height_px)

    def paintEvent(self,event):
        if self.paint_error_occurred:
            return
        try:
            painter = QPainter(self)

            driver = DrawingDriverQt(painter, self.anim_context.settings)
            self.anim_context.driver(driver)

            window_rect = QRectF(0, 0, self.anim_context.settings.window_with_px, self.anim_context.settings.window_height_px)
            painter.fillRect(window_rect, QColor(self.anim_context.settings.background_color))

            self.anim_context.draw_frame()

            self.anim_context.driver(None)
        except Exception:
            self.paint_error_occurred = True
            print("Unexpected exception:")
            print(traceback.format_exc())
        finally:
            painter.end()

class AnimForm(QDialog):

    ST_STOPPED = 1
    ST_PAUSED = 2
    ST_PLAYING = 3
    ST_ENDED = 4

    def __init__(self, parent, anim_context: AnimContext):
        super().__init__(parent)
        self.anim_context = anim_context
        self.input_getters: Dict[str,Callable[[],float]] = dict()
        self.timer_error_occurred = False
        self.anim_state = self.ST_STOPPED

        self.setWindowTitle(os.path.basename(sys.argv[0]))
        self.renderArea = AnimRenderArea(self, anim_context)
        layout = QGridLayout()
        self.createMediaButtonsBox()
        layout.addWidget(self.mediaButtonsBox, 0,0,1,1, Qt.AlignLeft)
        self.createVarsBox()
        if anim_context.vars._input_vars:
            layout.addWidget(self.varsBox,0,1,1,1, Qt.AlignRight)
        layout.addWidget(self.renderArea,1,0,1,2)
        self.setLayout(layout)

        self.resetAnimation()

    def createMediaButtonsBox(self):
        self.playPauseButton = QPushButton()
        font = self.playPauseButton.font()
        font.setPointSize(10)
        self.playPauseButton.setFont(font)
        self.playPauseButton.clicked.connect(self.playPauseButtonClicked) 

        self.stopButton = QPushButton()
        self.stopButton.setFont(font)
        self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopButton.setText("Stop")
        self.stopButton.clicked.connect(self.stopButtonClicked)

        layout = QGridLayout()
        layout.addWidget(self.playPauseButton,0,0)
        layout.addWidget(self.stopButton,0,1)

        self.mediaButtonsBox = QGroupBox()
        self.mediaButtonsBox.setLayout(layout)

    def createVarsBox(self):
        layout = QGridLayout()
        next_grid_row = 0

        for var_name, var_meta in self.anim_context.vars._input_vars.items():
            var_label = QLabel(f"{var_name} =")
            font = var_label.font()
            font.setPointSize(10)
            var_label.setFont(font)
            layout.addWidget(var_label, 0, next_grid_row, Qt.AlignRight)

            if isinstance(var_meta, InputFloat): 
                var_box = QDoubleSpinBox()
                var_box.setDecimals(2)
                var_box.setStepType(QDoubleSpinBox.StepType.AdaptiveDecimalStepType)
                var_box.setRange(var_meta.limit_from, var_meta.limit_to)
                var_box.setValue(var_meta.default)
                var_box.valueChanged.connect(self.inputVarChanged)
                self.input_getters[var_name] = lambda vsb=var_box: vsb.value()
            elif isinstance(var_meta, InputList):
                var_box = QComboBox()
                for i,v in enumerate(var_meta.lov):
                    var_box.addItem(str(v))
                    if v == var_meta.default:
                        var_box.setCurrentIndex(i)
                var_box.currentIndexChanged.connect(self.inputVarChanged)
                self.input_getters[var_name] = lambda vsb=var_box, t=type(var_meta.default): t(vsb.currentText())
            var_box.setFont(font) 
            layout.addWidget(var_box, 0, next_grid_row + 1 , Qt.AlignLeft)
            next_grid_row +=2


        self.varsBox = QGroupBox()
        self.varsBox.setLayout(layout)


    def resetAnimation(self):
        self.anim_state = self.ST_STOPPED
        input_getters: Dict[str,Callable[[],float]] = self.input_getters
        self.anim_context.reset(input_getters)
        self.playPauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playPauseButton.setText("Play")
        self.varsBox.setEnabled(True)
        self.playPauseButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.renderArea.update()
    
    def playAnimation(self):
        self.anim_state = self.ST_PLAYING
        self.playPauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.playPauseButton.setText("Pause")
        self.varsBox.setEnabled(False)
        self.stopButton.setEnabled(False)
        w_sec = self.anim_context.settings.frame_period
        self.target_frame_time = time.time() + w_sec
        w_msec = int(round(w_sec*1000))
        QTimer.singleShot(w_msec, self.frameTimerEvent)

    def pauseAnimation(self):
        self.anim_state = self.ST_PAUSED
        self.playPauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playPauseButton.setText("Play")
        self.stopButton.setEnabled(True)

    def endAnimation(self):
        self.anim_state = self.ST_ENDED
        self.playPauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playPauseButton.setText("Play")
        self.stopButton.setEnabled(True)
        self.playPauseButton.setEnabled(False)



    def frameTimerEvent(self):
        if self.timer_error_occurred:
            return
        try:
            now0 = time.time_ns() / 1000000000
            #now0 = time.time()
            fp = self.anim_context.settings.frame_period
            #print(f"{now0 - (self.target_frame_time -fp):7.4f}", end=", ")
            if self.anim_state in (self.ST_STOPPED, self.ST_ENDED):
                return
            if self.anim_state == self.ST_PLAYING:
                cont = self.anim_context.updates_between_frames()
                if not cont:
                    self.endAnimation()
                self.renderArea.repaint()

            now = time.time_ns() / 1000000000
            #now = time.time()
            #print(f"{(now-now0):7.4f}", end=", ")

            self.target_frame_time = now0 + fp 
            wait_time = self.target_frame_time - now
            #print(f"{wait_time:7.4f}")
            w_int = int(round(wait_time*1000))
            if w_int <= 0:
                w_int = 1
            QTimer.singleShot(w_int, Qt.PreciseTimer, self, SLOT("frameTimerEvent()"))

        except Exception:
            self.timer_error_occurred = True
            print("Unexpected exception:")
            print(traceback.format_exc())

    def playPauseButtonClicked(self, event):
        if self.anim_state == self.ST_PLAYING:
            self.pauseAnimation()
        else:
            self.playAnimation()
            
    def stopButtonClicked(self, event):
        self.resetAnimation()

    def inputVarChanged(self, event):
        if self.anim_state == self.ST_STOPPED:
            self.resetAnimation()



    def export_movie(self):
        def do_export_movie():
            pass # TODO https://stackoverflow.com/questions/24961127/how-to-create-a-video-from-images-with-ffmpeg
                 # https://superuser.com/questions/1429256/producing-lossless-video-from-set-of-png-images-using-ffmpeg
        contextvars.copy_context().run(do_export_movie)
        

def Run(setup_handler:Callable[[AnimVars], None], update_handler:Callable[[AnimVars], None], draw_handler:Callable[[AnimVars], None]):
    anim_context = AnimContext(setup_handler, update_handler, draw_handler)
    app = QApplication()
    form = AnimForm(None,anim_context)
    form.show()
    app.exec_()