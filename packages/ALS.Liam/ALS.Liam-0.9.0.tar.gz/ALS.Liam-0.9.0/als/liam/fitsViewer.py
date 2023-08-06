# -*- coding: utf-8 -*-

import sip
sip.setapi('QVariant', 2)	# Call this before referencing QtCore
sip.setapi('QString', 2)	# Call this before referencing QtCore

# from PyQt4 import QtGui, QtCore
# from PyQt4.QtCore import Qt, QString, QVariant, QRect, QRectF, QSize, QPoint
from PyQt4.QtCore import Qt, QRect, QRectF, QSize, QPoint
from PyQt4.QtCore import QObject, SIGNAL, SLOT, QCoreApplication
from PyQt4.QtCore import QAbstractTableModel, QModelIndex
from PyQt4.QtGui import QApplication, QMainWindow, QTextEdit, QLabel, QStyle
from PyQt4.QtGui import QStyledItemDelegate, QStyleOptionViewItemV4
from PyQt4.QtGui import QTextDocument, QPushButton, QStyleOptionButton
from PyQt4.QtGui import QStyleFactory, QGraphicsProxyWidget, QCheckBox
from PyQt4.QtGui import QSizePolicy, QFileDialog, QPalette, QColor
from PyQt4.QtGui import QHeaderView
# from PyQt4.QtGui import QCommonStyle, QCleanlooksStyle, QPlastiqueStyle
# from PyQt4.QtGui import QMacStyle, QWindowsStyle, QWindowsXPStyle
import pyqtgraph as pg
import als.liam.fitsViewerGui as fitsViewerGui
from als.liam.fitsParams import fitsParamsModel
from als.liam.fitsParams import qtFloatDelegate, qtHtmlDelegate
from als.liam.fitsParams import qtDateDelegate, qtTimeDelegate
from als.liam.fitsParams import fitsParamsLeftColModel, fitsParamsRightColModel

from PIL import Image
from numpy import nan, float32, sqrt, round, floor, array, log10
from numpy.random import random_integers, randint
from astropy.io import fits
import pandas as pd

import os
import sys
from als.milo.qimage import Diffractometer402, CcdImageFromFITS

try:
     #_fromUtf8 = QString.fromUtf8
    pass
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


pg.setConfigOptions(imageAxisOrder="row-major")


def show_motor_params(primary_hdu):
	# print 'Beamline Energy   : ' + str(primary_hdu['Beamline Energy']) + ' eV'
	print 'Mono Energy   : ' + str(primary_hdu['Mono Energy']) + ' eV'
	print 'Bottom Rotary Seal: ' + str(primary_hdu['Bottom Rotary Seal']) + ' deg'
	print 'Top Rotary Seal   : ' + str(primary_hdu['Top Rotary Seal']) + ' deg'
	print 'Flip              : ' + str(primary_hdu['Flip']) + ' deg'
	print 'Twice Top Offset  : ' + str(primary_hdu['Twice Top Offset']) + ' deg'
	
	# energy = primary_hdu['Beamline Energy']
	energy = primary_hdu['Mono Energy']
	bottom = primary_hdu['Bottom Rotary Seal']
	top = primary_hdu['Top Rotary Seal']
	flip = primary_hdu['Flip']
	offset_top = primary_hdu['Twice Top Offset'] / 2
	offset_flip = 0
	offset_ccd = -18.68
	
	if ('Top Offset' in primary_hdu):
		offset_top = primary_hdu['Top Offset']
		print 'Top Offset        : ' + str(offset_top) + ' deg'
	if ('Flip Offset' in primary_hdu):
		offset_flip = primary_hdu['Flip Offset']
		print 'Flip Offset       : ' + str(offset_flip) + ' deg'
	if ('CCD Offset' in primary_hdu):
		offset_ccd = primary_hdu['CCD Offset']
		print 'CCD Offset        : ' + str(offset_ccd) + ' deg'
		
	wavelength = 1239.842 / energy
	twotheta = bottom - offset_ccd
	truetop = top - offset_top
	incidence = bottom - truetop
	chi = flip - offset_flip
	
	print ''
	print 'Wavelength : ' + str(wavelength) + ' nm'
	print 'Detector   : ' + str(twotheta) + ' deg'
	print 'Incidence  : ' + str(incidence) + ' deg'
	print 'Chi        : ' + str(chi) + ' deg'


def load_image(filename):
	hdulist = fits.open(filename)
# 	print "We opened an image. It's filename is ", filename
# 	print "here's some info"
# 	print hdulist.info()
	
	# show_motor_params(hdulist[0].header)
	
	# let's assume, the last entry is the image.
	return (hdulist[0].header, hdulist[-1])
	

class FitsViewerApp(QMainWindow, fitsViewerGui.Ui_MainWindow):
	def __init__(self, parent=None):
		super(FitsViewerApp, self).__init__(parent)
		self.setupUi(self)
		
		self.setWindowTitle(
			_translate("MainWindow", "FITS data viewer", None))
		
		glImage = self.glFitsImage
		
		glBoxImageTitle = (0, 0, 1, 3)
		glBoxImageSubtitle = (1, 0, 1, 3)
		glBoxPlotRows = (2, 0)
		glBoxImageView = (2, 1)
		glBoxLutHistog = (2, 2)
		glBoxPlotCols = (3, 1)
		glBoxColorScaling = (3, 2)
		
		self.txtImageTitle = pg.LabelItem(
			"Click 'Load data file' button to begin...", size='24pt')
		self.txtImageSubtitle = pg.LabelItem("Default data displayed")
		glImage.addItem(self.txtImageTitle, *glBoxImageTitle)
		glImage.addItem(self.txtImageSubtitle, *glBoxImageSubtitle)
		self.txtImageTitle.setSizePolicy(
			QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
		self.txtImageSubtitle.setSizePolicy(
			QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
		
		self.image_array = randint(512, 2**16, size=(512, 512))
		image_array = self.image_array
		(imgRows, imgCols) = image_array.shape
		
		self.imv = glImage.addViewBox(*glBoxImageView)
		imv = self.imv
		# imv.invertY(True)		# Need to invert if image is not FITS
		img = pg.ImageItem(image_array, border=0.5)
		self.image = img
		self.image.setCursor(Qt.CrossCursor)
		imv.addItem(img)
		imv.setAspectLocked()
# 		imv.setLimits(
# 			maxXRange=imgCols, maxYRange=imgRows, 
# 			xMin=0, xMax=imgCols, yMin=0, yMax=imgRows, 
# 			)
		self.linRegRows = pg.LinearRegionItem(
			values=[0, 0], 
			orientation=pg.LinearRegionItem.Horizontal, 
			brush=(0, 0, 255, 64), 
			# pen='b', 
			bounds=(0, imgRows), 
			)
		self.linRegCols = pg.LinearRegionItem(
			values=[0, 0], 
			orientation=pg.LinearRegionItem.Vertical, 
			brush=(255, 255, 0, 64), 
			# pen = 'y', 
			bounds=(0, imgCols), 
			)
		imv.addItem(self.linRegRows)
		imv.addItem(self.linRegCols)
		# imv.setPredefinedGradient("flame")
		# imv.setLookupTable(xxx)
		# vbLutHistog = glImage.addViewBox(0, 1)
		self.lutHistog = pg.HistogramLUTItem(img)
		lutHistog = self.lutHistog
		# lutHistog.setImageItem(img)
		lutHistog.plot.rotate(-90)
		lutHistog.plot.setLogMode(False, True)
		lutHistog.plot.rotate(90)
		# lutHistog.sigLevelsChanged.connect(self.onImageLevelsChanged)
		lutHistog.sigLevelChangeFinished.connect(self.onImageLevelsChanged)
		lutHistog.gradient.loadPreset("flame")
		glImage.addItem(lutHistog, *glBoxLutHistog)
		# viewLutHistog = glImage.addViewBox(0, 2)
		# viewLutHistog.addItem(lutHistog)
		self.plotFitsRows = glImage.addPlot(*glBoxPlotRows)
		self.plotFitsCols = glImage.addPlot(*glBoxPlotCols)
		self.plotFitsRowsData = self.plotFitsRows.plot(
			image_array.mean(axis=1), 
			fillLevel=image_array.min(), 
			# -image_array.mean(axis=1), 
			# fillLevel = -(image_array.min()), 
			# fillLevel = (-image_array.astype(int)).max(), 
			fillBrush='y')
		self.plotFitsRowsData.scale(-1, 1)
		self.plotFitsRowsData.rotate(90)
		self.plotFitsRows.setYLink(imv)
		self.plotFitsRows.invertX(True)
		# self.plotFitsRows.invertY(True)
		self.plotFitsColsData = self.plotFitsCols.plot(
			image_array.mean(axis=0), 
			fillLevel=image_array.min(), 
			fillBrush='b')
		self.plotFitsCols.setXLink(imv)
		# self.plotFitsRows.rotate(90)
		glImage.ci.layout.setColumnMaximumWidth(glBoxPlotRows[1], 100)
		glImage.ci.layout.setRowMaximumHeight(glBoxPlotCols[0], 100)
		
		glImageScale = pg.GraphicsLayout()
		
		proxy = QGraphicsProxyWidget()
		self.chkAutoScale = QCheckBox('Auto scale')
		self.chkAutoScale.setChecked(True)
		self.chkAutoScale.stateChanged.connect(self.onAutoScaleChanged)
# 		self.chkAutoScale.setSizePolicy(
# 			QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
		proxy.setWidget(self.chkAutoScale)
		glImageScale.addItem(proxy, 0, 0)
		
		proxy = QGraphicsProxyWidget()
		# self.chkLogScale = QCheckBox('Log scale', self)
		self.chkLogScale = QCheckBox('Log scale')
		self.chkLogScale.setChecked(False)
		self.chkLogScale.stateChanged.connect(self.onLogScaleChanged)
# 		self.chkLogScale.setSizePolicy(
# 			QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
		proxy.setWidget(self.chkLogScale)
		glImageScale.addItem(proxy, 1, 0)
		
		glImageScale.setSizePolicy(
			QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
		
		glImage.addItem(glImageScale, *glBoxColorScaling)
		
# 		SLOT('onLinRegColsChanged(QObject)')
# 		SLOT('onLinRegRowsChanged(QObject)')
		
		self.linRegCols.sigRegionChanged.connect(self.onLinRegColsChanged)
		self.linRegRows.sigRegionChanged.connect(self.onLinRegRowsChanged)
# 		QObject.connect(
# 			# self.linRegCols, SIGNAL('sigRangeChanged(QObject)'), 
# 			self.linRegCols, SIGNAL('sigRangeChanged'), 
# 			self.onLinRegColsChanged)
# 		QObject.connect(
# 			# self.linRegRows, SIGNAL('sigRangeChanged(QObject)'), 
# 			self.linRegRows, SIGNAL('sigRangeChanged'), 
# 			self.onLinRegRowsChanged)
		
		imv.autoRange()
		
		self.spinDataFrameNum.setMinimum(0)
		self.spinDataFrameNum.setMaximum(0)
		
		self.image_cursor_label = None
		img.scene().sigMouseMoved.connect(self.onMouseMoved)
		
		self.btnSelectDataFile.clicked.connect(self.selectDataFile)
		self.btnReloadDataFile.clicked.connect(self.loadDataFile)
		
		self.spinDataFrameNum.valueChanged.connect(self.updateDataFrame)
		
		self.btnFirstDataFrame.clicked.connect(self.gotoFirstDataFrame)
		self.btnPrevDataFrame.clicked.connect(self.gotoPrevDataFrame)
		self.btnNextDataFrame.clicked.connect(self.gotoNextDataFrame)
		self.btnLastDataFrame.clicked.connect(self.gotoLastDataFrame)
		
		# Project directory is parent of "als/liam/"
		self.project_directory = os.path.dirname(
			os.path.dirname(
				os.path.dirname(
					os.path.abspath(__file__) 
					) 
				)
			)
		self.data_directory = "{}/test_data/".format(self.project_directory)
		self.working_directory = str(self.data_directory)
		self.data_pathnames = []
		self.data_frame_num = 0
		# self.selectDataFile()
		
# 		palSelectButton = QPalette()
# 		palSelectButton.setColor(QPalette.Button, QColor(Qt.yellow))
# 		self.btnSelectDataFile.setAutoFillBackground(True)
# 		self.btnSelectDataFile.setPalette(palSelectButton)

		self.cbPauseParamUpdates.setChecked(False)
		self.cbPauseParamUpdates.stateChanged.connect(
			self.onPauseFitsParamsUpdatesChanged)
		
		self.model_fits_params_left = fitsParamsLeftColModel()
		
		self.viewFitsParamsLeft.setModel(self.model_fits_params_left)
		self.viewFitsParamsLeft.setItemDelegateForColumn(
			0, 
			qtHtmlDelegate(self) )
		self.viewFitsParamsLeft.setItemDelegateForColumn(
			1, 
			qtFloatDelegate(self, decimals=3) )
		self.viewFitsParamsLeft.setItemDelegateForColumn(
			2, 
			qtHtmlDelegate(self) )
			
		self.viewFitsParamsLeft.resizeColumnsToContents()
		
		self.viewFitsParamsLeft.horizontalHeader().setResizeMode(
			1, QHeaderView.Stretch)
		self.viewFitsParamsLeft.horizontalHeader().setDefaultAlignment(
			Qt.AlignRight)
		self.viewFitsParamsLeft.horizontalHeader().hide()
		self.viewFitsParamsLeft.verticalHeader().hide()
# 		self.viewFitsParamsLeft.setHorizontalScrollBarPolicy(
# 			Qt.ScrollBarAlwaysOff)
# 		self.viewFitsParamsLeft.setVerticalScrollBarPolicy(
# 			Qt.ScrollBarAlwaysOff)
		# self.viewFitsParamsLeft.adjustSize()
		
		fitsParamsRightColModel
		
		self.model_fits_params_right = fitsParamsRightColModel()
		
		self.viewFitsParamsRight.setModel(self.model_fits_params_right)
		self.viewFitsParamsRight.setItemDelegateForColumn(
			0, 
			qtHtmlDelegate(self) )
		self.viewFitsParamsRight.setItemDelegateForColumn(
			1, 
			qtFloatDelegate(self, decimals=3) )
		self.viewFitsParamsRight.setItemDelegateForColumn(
			2, 
			qtHtmlDelegate(self) )
			
		self.viewFitsParamsRight.resizeColumnsToContents()
		
		self.viewFitsParamsRight.horizontalHeader().setResizeMode(
			1, QHeaderView.Stretch)
		self.viewFitsParamsRight.horizontalHeader().setDefaultAlignment(
			Qt.AlignRight)
		self.viewFitsParamsRight.horizontalHeader().hide()
		self.viewFitsParamsRight.verticalHeader().hide()
		
		self.viewFitsParamsRight.setSpan(0, 0, 1, 3)
		self.viewFitsParamsRight.setSpan(1, 0, 1, 3)
		self.viewFitsParamsRight.setItemDelegateForRow(
			0, 
			qtDateDelegate(self) )
		self.viewFitsParamsRight.setItemDelegateForRow(
			1, 
			qtTimeDelegate(self) )
		
		# self.setStyleSheet(".sub { vertical-align: sub }")
		# self.setStyleSheet(".sup { vertical-align: super }")
	
	def onLinRegColsChanged(self, linReg):
		
		# self.plotFitsRows.setYRange(linReg.getRegion())
		image_array = self.image_array
		(minCol, maxCol) = linReg.getRegion()
		(minCol, maxCol) = (int(round(minCol)), int(round(maxCol)))
		if (minCol == maxCol):
			minCol = 0
			maxCol = image_array.shape[1]
		# print "onLinRegRowsChanged:", linReg.getRegion()
		self.plotFitsRowsData.setData(image_array[:, minCol:maxCol].mean(axis=1))
		# self.plotFitsRowsData.setData(-image_array[:, minCol:maxCol].mean(axis=1))
	
	def onLinRegRowsChanged(self, linReg):
		
		# self.plotFitsCols.setXRange(linReg.getRegion())
		image_array = self.image_array
		(minRow, maxRow) = linReg.getRegion()
		(minRow, maxRow) = (int(round(minRow)), int(round(maxRow)))
		if (minRow == maxRow):
			minRow = 0
			maxRow = image_array.shape[0]
		# print "onLinRegColsChanged:", linReg.getRegion()
		self.plotFitsColsData.setData(image_array[minRow:maxRow].mean(axis=0))
	
	def onLogScaleChanged(self, state):
		
		log_mode = (state & Qt.Checked)
		
		lutHistog_levels = self.lutHistog.getLevels()
# 		if self.lutHistog.axis.logMode:
# 			lutHistog_levels = 10 ** array(lutHistog_levels)
		
		image_array = self.image_array
		if log_mode:
			image_array = log10(self.image_array)
			lutHistog_levels = log10(lutHistog_levels)
		else:
			lutHistog_levels = 10 ** array(lutHistog_levels)
		fill_level = image_array.min()
		self.plotFitsRows.getAxis("bottom").setLogMode(log_mode)
		self.plotFitsCols.getAxis("left").setLogMode(log_mode)
		
		self.plotFitsRowsData.rotate(-90)
		self.plotFitsRowsData.setLogMode(False, log_mode)
		self.plotFitsRowsData.setFillLevel(fill_level)
		self.plotFitsRowsData.rotate(90)
		
		self.plotFitsColsData.setLogMode(False, log_mode)
		self.plotFitsColsData.setFillLevel(fill_level)
		
		lutHistog = self.lutHistog
		lutHistog.sigLevelChangeFinished.disconnect(self.onImageLevelsChanged)
		self.image.setImage(image_array)
		self.lutHistog.setLevels(*lutHistog_levels)
		self.lutHistog.axis.setLogMode(log_mode)
		lutHistog.sigLevelChangeFinished.connect(self.onImageLevelsChanged)
	
	def onAutoScaleChanged(self, state):
		
		auto_scale_mode = (state & Qt.Checked)
		log_mode = self.chkLogScale.isChecked()
		
		image_array = self.image_array
		if log_mode:
			image_array = log10(self.image_array)
		
		if auto_scale_mode:
			self.lutHistog.sigLevelChangeFinished.disconnect(
				self.onImageLevelsChanged)
			self.lutHistog.autoHistogramRange()
			self.lutHistog.setLevels(image_array.min(), image_array.max())
			self.lutHistog.sigLevelChangeFinished.connect(
				self.onImageLevelsChanged)
	
	def onImageLevelsChanged(self, lutHistog):
	
		self.chkAutoScale.setChecked(False)
		
# 		log_mode = self.chkLogScale.isChecked()
# 		
# 		lutHistog_levels = lutHistog.getLevels()
# 		print "lutHistog_levels:", lutHistog_levels
# 		# if lutHistog.axis.logMode:
# 		if log_mode:
# 			lutHistog_levels = 10 ** array(lutHistog_levels)
# 			print "[LOG] lutHistog_levels:", lutHistog_levels
# 		
# 		# self.image
# 		print "getLevels():", lutHistog.imageItem().getLevels()
# 		lutHistog.imageItem().setLevels(lutHistog_levels)
# 		print "[AFTER] getLevels():", lutHistog.imageItem().getLevels()
# 		# lutHistog.update()

	def onPauseFitsParamsUpdatesChanged(self, state):

		if self.data_pathnames:
			self.loadDataFile()
	
	def keyPressEvent(self, keyEvent):
		
		if ((
				(keyEvent.key() == Qt.Key_Q) and 
				(keyEvent.modifiers() == Qt.ControlModifier)
				) or 
			(
				(keyEvent.key() == Qt.Key_W) and 
				(keyEvent.modifiers() == Qt.ControlModifier)
				)):
			print "QUIT"
			QCoreApplication.instance().quit()
	
	def onMouseMoved(self, event):
		
		# pos = event.pos()
		pos = [event.x(), event.y()]
		
		if self.image.sceneBoundingRect().contains(event):
		
			# self.image.setCursor(Qt.CrossCursor)
			view_pos = self.imv.mapToView(event)
# 			image_pos = self.imv.mapFromViewToItem(
# 				self.image, view_pos)
			image_pos = self.image.mapFromScene(event)
			# print "\nEvent Pos:", event
			# print "\tView Pos:", view_pos
			# print "\tImage Pos:", image_pos
			# pos = [event.x(), event.y()]
			# pos = [view_pos.x(), view_pos.y()]
			pos = [image_pos.x(), image_pos.y()]
			# coords = tuple([int(round(coord)) for coord in pos])
			coords = tuple([int(floor(coord)) for coord in pos])
			# coord_text = "({0:d}, {1:d})".format(*coords)
			coord_text = "(r:{1:d}, c:{0:d})".format(*coords)
			coord_text += "\nIntemsity:{0:0,.0f}".format(
				self.image_array[coords[1], coords[0]],
				)
			self.image.setToolTip(coord_text)
			
# 			if self.image_cursor_label is None:
# 				label = pg.TextItem(coord_text, anchor=(1,0), fill=(0,0,0,80))
# 				label.setParentItem(self.image)
# 				# label.setPos(*coords)
# 				# label.setPos(event)
# 				# label.setPos(view_pos)
# 				label.setPos(image_pos)
# 				self.image_cursor_label = label
# 			else:
# 				label = self.image_cursor_label
# 				label.setText(coord_text)
# 				# label.setPos(*coords)
# 				# label.setPos(event)
# 				# label.setPos(view_pos)
# 				label.setPos(image_pos)
# 			anchor_point = [1, 0]
# 			if not label.viewRect().contains(
# 					label.boundingRect().topLeft() ):
# 				anchor_point[0] = 0
# 			if not label.viewRect().contains(
# 					label.boundingRect().bottomRight() ):
# 				anchor_point[1] = 1
# 			label.setAnchor(anchor_point)
# 		else:
# 			if self.image_cursor_label is not None:
# 				self.image_cursor_label.scene().removeItem(
# 					self.image_cursor_label)
# 				self.image_cursor_label = None
	
	def selectDataFile(self):
		
		# data_pathname = "{}Log_NiFe_00d_1340-060.fits".format(self.data_directory)
# 		data_pathname = "{}NiFe_00d_1340-060.fits".format(self.data_directory)
# 		self.data_pathnames = [data_pathname]
# 		self.data_frame_num = 1
		
# 		png_filename = "{}NiFe_00d_1340-060.png".format(self.data_directory)
# 		self.image_array = array(Image.open(png_filename))
# 		# self.image_array = array(Image.open(png_filename).convert("L"))
# 		# print "self.image_array:", self.image_array
# 		# print "self.image_array.shape:", self.image_array.shape
# 		# exit()
		
		# QFileDialog.setFileMode(QFileDialog.ExistingFile)
		selected_pathname = str(QFileDialog.getOpenFileName(
			self, 
			"Select data file", 
			self.working_directory, 
			# "FITS (*.fits);; Images (*.png *.jpg *.jpeg *.gif *.tiff);; AI files (*-AI.txt)")
			"FITS, PNG, AI files (*.fits *.png *-AI.txt)")
			)
		
		# print "selected_pathname:", selected_pathname
		
		self.raise_()
		self.activateWindow()
		
		data_frame_num = self.data_frame_num
		selected_pathname_parts = selected_pathname.split('/')
		data_path = "/".join(selected_pathname_parts[:-1])
		self.working_directory = data_path
		
		if selected_pathname.endswith("-AI.txt"):
		
# 			data_file = open(selected_pathname, 'r')
# 			file_line = data_file.readline().rstrip('\r\n')
# 			imgscan_header_linenum = 0
# 			while not file_line.startswith("Frame"):
# 				file_line = data_file.readline().rstrip('\r\n')
# 				imgscan_header_linenum++
# 			data_file.close()
			
			with open(selected_pathname, 'r') as data_file:
				for (header_linenum, file_line) in enumerate(data_file):
					# print (header_linenum, file_line)
					if file_line.startswith("Frame"):
						break
					if file_line[0].isdigit():
						header_linenum -= 1
			
			# check for missing header line
			# print "header_linenum:", header_linenum

			# header_linenum = 9
			imgscan_data = pd.read_table(
				selected_pathname,
				delimiter='\t',
				header=header_linenum,
				skip_blank_lines=False,
				)
			# imgscan_num_rows = len(imgscan_data)

			self.data_pathnames = ["{0:s}/WinView CCD/{1:s}.fits".format(
				data_path,
				filename,
				) for filename in imgscan_data['PNG Image filename'] ]
			
			if (self.data_frame_num > len(self.data_pathnames) ):
				# self.data_frame_num = len(self.data_pathnames)
				data_frame_num = len(self.data_pathnames)
		
		else:
			
			self.data_pathnames = [selected_pathname]
			# self.data_frame_num = 1
			data_frame_num = 1
		
		self.editDataFilename.setText(selected_pathname)
		self.spinDataFrameNum.setMinimum(1)
		self.spinDataFrameNum.setMaximum(len(self.data_pathnames))
		# self.spinDataFrameNum.setValue(self.data_frame_num)
		self.spinDataFrameNum.setValue(data_frame_num)
		
		self.loadDataFile(fullView=True)
	
	def loadDataFile(self, fullView=False):
		
		data_pathname = self.data_pathnames[self.data_frame_num - 1]
		
		# print "data_pathname:", data_pathname
		
		data_pathname_parts = data_pathname.split('/')
		data_path = " / ".join(data_pathname_parts[:-1])
		data_filename = data_pathname_parts[-1]
		
		self.txtImageTitle.setText(data_filename)
		self.txtImageSubtitle.setText(data_path)
		
		if data_filename.lower().endswith(".fits"):
		
			# hdu_pair    = load_image(data_pathname)
			# hdu_header  = hdu_pair[0]
			# hdu_image   = hdu_pair[-1]
			
			hdulist = fits.open(data_pathname)
			ccd_image = CcdImageFromFITS(
				hdulist,
				# offset_diffractometer = offset_angles
				)

			# self.image_array = hdu_image.data
			self.image_array = ccd_image.data
			self.imv.invertY(False)		# Need to invert if image is not FITS
			
			if self.cbPauseParamUpdates.isChecked():
				self.updateFitsParameters(None)
			else:
				self.updateFitsParameters(ccd_image)
		
		else:
		
			self.image_array = array(Image.open(data_pathname))
			self.imv.invertY(True)		# Need to invert if image is not FITS
			
			self.updateFitsParameters(None)
		
		image_array = self.image_array
		log_mode = self.chkLogScale.isChecked()
		if log_mode:
			image_array = log10(self.image_array)
		(imgRows, imgCols) = image_array.shape
			
		self.image.setImage(image_array)
		self.image.setLevels(self.lutHistog.getLevels())
		self.linRegRows.setBounds((0, imgRows))
		self.linRegCols.setBounds((0, imgCols))
		fill_level = image_array.min()
		self.plotFitsRowsData.setFillLevel(fill_level)
		self.plotFitsColsData.setFillLevel(fill_level)
		if fullView:
			self.imv.autoRange()
		self.onLinRegRowsChanged(self.linRegRows)
		self.onLinRegColsChanged(self.linRegCols)
	
	def updateDataFrame(self, value):
		
		self.data_frame_num = int(value)
		self.loadDataFile()
	
	def gotoFirstDataFrame(self):
		
		self.spinDataFrameNum.setValue(self.spinDataFrameNum.minimum())
	
	def gotoPrevDataFrame(self):
		
		self.spinDataFrameNum.stepDown()
	
	def gotoNextDataFrame(self):
		
		self.spinDataFrameNum.stepUp()
	
	def gotoLastDataFrame(self):
		
		self.spinDataFrameNum.setValue(self.spinDataFrameNum.maximum())
	
	def updateFitsParameters(self, ccdImage=None):
		
		self.model_fits_params_left.loadParams(ccdImage)
		self.model_fits_params_right.loadParams(ccdImage)

def main():
	app = QApplication(sys.argv)
# 	print "QStyleFactory.keys():", [str(s) for s in QStyleFactory.keys()]
# 	print "app.style():", app.style(), type(app.style())
# 	print QApplication.style().metaObject().className(), "\n"
# 	for key in QStyleFactory.keys():
# 		st = QStyleFactory.create(key)
# 		print key, st.metaObject().className(), type(app.style())
	# app.setStyle("Windows")
	mainWin = FitsViewerApp()
	mainWin.show()
	mainWin.raise_()
	# mainWin.activateWindow()
	app.exec_()

if __name__ == '__main__':
    main()