# -*- coding: utf-8 -*-

import sip
sip.setapi('QVariant', 2)	# Call this before referencing QtCore
sip.setapi('QString', 2)	# Call this before referencing QtCore

# from PyQt4 import QtGui, QtCore
# from PyQt4.QtCore import Qt, QString, QVariant, QRect, QRectF, QSize, QPoint
from PyQt4.QtCore import Qt, QRect, QRectF, QSize, QPoint
from PyQt4.QtCore import QAbstractTableModel, QModelIndex
from PyQt4.QtGui import QApplication, QMainWindow, QTextEdit, QLabel, QStyle
from PyQt4.QtGui import QStyledItemDelegate, QStyleOptionViewItemV4
from PyQt4.QtGui import QTextDocument, QPushButton, QStyleOptionButton
from PyQt4.QtGui import QStyleFactory
# from PyQt4.QtGui import QCommonStyle, QCleanlooksStyle, QPlastiqueStyle
# from PyQt4.QtGui import QMacStyle, QWindowsStyle, QWindowsXPStyle

from datetime import datetime, date

from numpy import nan, float32, sqrt, array, isnan
import pandas as pd
import itertools as it

import sys
from als.milo.qimage import Diffractometer402, CcdImageFromFITS, Polarization

try:
    # _fromUtf8 = QString.fromUtf8
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

# ----------------------------------------------------------------
# ----------------------------------------------------------------
class fitsParamsModel(QAbstractTableModel):
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def __init__(self, parent=None, ccdImage=None):
		super(fitsParamsModel, self).__init__(parent)
		
		self.numRows = 0
		self.numCols = 3
		
		labels = []
		values = []
		units = []
		
		(
			self.labels_col, 
			self.values_col, 
			self.units_col, 
			) = range(self.numCols)
		
		self.df = pd.DataFrame(
			{
				"label": labels, 
				"value": values, 
				"unit": units, 
				}, 
			)
		self.df = self.df.reindex_axis([
			"label", 
			"value", 
			"unit", 
			], axis=1)
		
		self.loadParams(ccdImage)
		
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
	def loadParams(self, ccdImage=None):
		
		self.ccdImage = ccdImage
		
		if ccdImage is None:
			self.df.loc[:, "value"] = nan
			self.dataChanged.emit(
				self.index(0, self.values_col), 
				self.index(len(self.df), self.values_col) )
			return()
		
		self.loadParamsFromCcdFits(ccdImage)
		self.dataChanged.emit(
			self.index(0, self.values_col), 
			self.index(len(self.df), self.values_col) )
		
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
	def clearParams(self):
		
		self.loadParams(ccdImage=None)
		
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
	def loadParamsFromCcdFits(self, ccdImage):
		
		return()
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
	def rowCount(self, parent=None):
		if (parent is None) or (parent == QModelIndex()):
			return(self.numRows)
		return(0)
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
	def columnCount(self, parent=None):
		if (parent is None) or (parent == QModelIndex()):
			return(self.numCols)
		return(0)
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
	def data(self, index, role = Qt.DisplayRole):
		if (role == Qt.DisplayRole):
			return self.df.iloc[index.row(), index.column()]
# 		if (role == Qt.TextAlignmentRole):
# 			if (index.column() == self.units_col):
# 				return Qt.AlignLeft
# 			else:
# 				return Qt.AlignRight
		return None

# ----------------------------------------------------------------
# ----------------------------------------------------------------
class fitsParamsLeftColModel(fitsParamsModel):
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
	def __init__(self, parent=None, ccdImage=None):
		super(fitsParamsLeftColModel, self).__init__(parent, ccdImage)
		
		table_contents = array([
			["Exposure time", nan, "sec."], 
			[" ", nan, " "], 
			[" ", nan, " "], 
			["Energy", nan, "eV"], 
			[" ", nan, " "], 
			["Detector, <i>2&theta;</i>", nan, "deg."], 
			["(2D) Incidence, <i>&alpha;</i>", nan, "deg."], 
			["(2D) Exit, <i>&beta;</i>", nan, "deg."], 
			["Transverse, <i>&chi;</i>", nan, "deg."], 
			[" ", nan, " "], 
			["X", nan, "mm"], 
			["Y", nan, "mm"], 
			["Z", nan, "mm"], 
			[" ", nan, " "], 
			# ["q<span class='sub'>X</span>", nan, "nm<span class='sup'>-1</span>"], 
			["q<sub>X</sub>", nan, "nm<sup>-1</sup>"], 
			["q<sub>Y</sub>", nan, "nm<sup>-1</sup>"], 
			["q<sub>Z</sub>", nan, "nm<sup>-1</sup>"], 
			])
		
		(self.numRows, self.numCols) = table_contents.shape
		
# 		(
# 			labels_col, 
# 			values_col, 
# 			units_col, 
# 			) = range(self.numCols)
		
		labels = table_contents[:, self.labels_col]
		values = table_contents[:, self.values_col]
		units = table_contents[:, self.units_col]
		
		blankline = it.count(0)
		indices = [
			"expTime", 
			"blank_{0:d}".format(blankline.next()), 
			"blank_{0:d}".format(blankline.next()), 
			"energy", 
			"blank_{0:d}".format(blankline.next()), 
			"twotheta", 
			"incidence2D", 
			"exit2D", 
			"transverse", 
			"blank_{0:d}".format(blankline.next()), 
			"x", 
			"y", 
			"z", 
			"blank_{0:d}".format(blankline.next()), 
			"qx", 
			"qy", 
			"qz", 
			]
		
		self.df = pd.DataFrame(
			{
				"label": labels, 
				"value": values, 
				"unit": units, 
				}, 
			index = pd.Index(indices), 
			)
		self.df = self.df.reindex_axis([
			"label", 
			"value", 
			"unit", 
			], axis=1)
		
		# print self.df["values"]
		# self.df["values"] = self.df["values"].astype(float32)
		# print self.df["values"]
		# print self.df
		
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
	def loadParamsFromCcdFits(self, ccdImage):
		
		diffractometer = ccdImage._diffractometer
		primary_hdu = ccdImage.hdulist[0].header
		qimage_df = ccdImage.qvalues_df()
		(num_rows, num_cols) = ccdImage.data.shape
		center_pixel = (
# 			(qimage_df["row"] == int(num_rows*(460./512.))) & 
			(qimage_df["row"] == int(num_rows - num_rows*(460./512.))) & 
			(qimage_df["col"] == int(num_cols/2.)) )
		
		self.df.loc["expTime", "value"] = ccdImage.exposure_time
		self.df.loc["energy", "value"] = diffractometer.energy
		self.df.loc["twotheta", "value"] = diffractometer.twotheta
		self.df.loc["incidence2D", "value"] = diffractometer.incidence
		self.df.loc["exit2D", "value"] = diffractometer.exit_angle
		self.df.loc["transverse", "value"] = diffractometer.transverse
		self.df.loc["x", "value"] = primary_hdu['X Position']
		self.df.loc["y", "value"] = primary_hdu['Y Position']
		self.df.loc["z", "value"] = primary_hdu['Z Position']
		self.df.loc["qx", "value"] = qimage_df.loc[center_pixel, "Qx"].values
		self.df.loc["qy", "value"] = qimage_df.loc[center_pixel, "Qy"].values
		self.df.loc["qz", "value"] = qimage_df.loc[center_pixel, "Qz"].values
		
		# print self.df["values"]
		# self.df["values"] = self.df["values"].astype(float32)
		# print self.df["values"]
		# print self.df

# ----------------------------------------------------------------
# ----------------------------------------------------------------
class fitsParamsRightColModel(fitsParamsModel):
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
	def __init__(self, parent=None, ccdImage=None):
		super(fitsParamsRightColModel, self).__init__(parent, ccdImage)
		
		table_contents = array([
			["Date", nan, " "], 
			["Timestamp", nan, " "], 
			[" ", nan, " "], 
			["Polarization", nan, " "], 
			[" ", nan, " "], 
			["Bottom Seal", nan, "deg."], 
			["Top Seal", nan, "deg."], 
			["Top Seal <i>offset</i>", nan, "deg."], 
			["Flip", nan, "deg."], 
			["Flip <i>offset</i>", nan, "deg."], 
			[" ", nan, " "], 
			["Temperature A", nan, "K"], 
			["Temperature B", nan, "K"], 
			[" ", nan, " "], 
			["|q|", nan, "nm<sup>-1</sup>"], 
			["q<sub>In-Plane</sub>", nan, "nm<sup>-1</sup>"], 
			["q<sub>Out-of-Plane</sub>", nan, "nm<sup>-1</sup>"], 
			])
		
		(self.numRows, self.numCols) = table_contents.shape
		
# 		(
# 			labels_col, 
# 			values_col, 
# 			units_col, 
# 			) = range(self.numCols)
		
		labels = table_contents[:, self.labels_col]
		values = table_contents[:, self.values_col]
		units = table_contents[:, self.units_col]
		
		blankline = it.count(0)
		indices = [
			"dateStamp", 
			"timeStamp".format(blankline.next()), 
			"blank_{0:d}".format(blankline.next()),
			"polarization".format(blankline.next()), 
			"blank_{0:d}".format(blankline.next()), 
			"bottom", 
			"top", 
			"topOffset", 
			"flip", 
			"flipOffset", 
			"blank_{0:d}".format(blankline.next()), 
			"tempA", 
			"tempB", 
			"blank_{0:d}".format(blankline.next()), 
			"qmag", 
			"qip", 
			"qop", 
			]
		
		self.df = pd.DataFrame(
			{
				"label": labels, 
				"value": values, 
				"unit": units, 
				}, 
			index = pd.Index(indices), 
			)
		self.df = self.df.reindex_axis([
			"label", 
			"value", 
			"unit", 
			], axis=1)
		
		# print self.df["values"]
		# self.df["values"] = self.df["values"].astype(float32)
		# print self.df["values"]
		# print self.df
		
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
	def loadParamsFromCcdFits(self, ccdImage):
		
		diffractometer = ccdImage._diffractometer
		primary_hdu = ccdImage.hdulist[0].header
		qimage_df = ccdImage.qvalues_df()
		(num_rows, num_cols) = ccdImage.data.shape
		center_pixel = (
			(qimage_df["row"] == int(num_rows*(460./512.))) & 
			(qimage_df["col"] == int(num_cols/2.)) )
			
		value = primary_hdu.get('DATE', None)
		if value is not None:
			if 'T' in value:
				image_date = datetime.strptime(value, 
					"%Y-%m-%dT%H:%M:%S").date()
				image_time = datetime.strptime(value, 
					"%Y-%m-%dT%H:%M:%S").time()
			else:
				image_date = datetime.strptime(value, "%Y-%m-%d").date()
				image_time = datetime.strptime(value, "%H:%M:%S").time()
		else:
			value = primary_hdu.get('DATETIME', None)
			if value is not None:
				image_date = datetime.strptime(value, 
					"%Y/%m/%d %H:%M:%S").date()
				image_time = datetime.strptime(value, 
					"%Y/%m/%d %H:%M:%S").time()
			else:
				image_date = datetime.strptime("1970-01-01", "%Y-%m-%d").date()
				image_time = datetime.strptime("1970-01-01", "%H:%M:%S").time()
		
		pol = diffractometer.polarization
		pol_state_text = dict({
			Polarization.UNDEFINED: "N/A",
			Polarization.CIRCULAR:	"Circ.",
			Polarization.LINEAR:	"Lin.", 
			})
		pol_value_text = dict({
			Polarization.UNDEFINED: nan,
			Polarization.CIRCULAR:	pol.circular_degree,
			Polarization.LINEAR:	pol.linear_angle, 
			})
		
		for key_entry in ('TempCtrlrA', 'Temperature A', 
						  'Lakeshore Temp Controller A', ):
			value = primary_hdu.get(key_entry, None)
			if value is not None:
				temperatureA = value
				break
		else:
			temperatureA = 298		# Kelvin
		
		for key_entry in ('TempCtrlrB', 'Temperature B', 
						  'Lakeshore Temp Controller B', ):
			value = primary_hdu.get(key_entry, None)
			if value is not None:
				temperatureB = value
				break
		else:
			temperatureB = 298		# Kelvin
		
		qxy = sqrt(qimage_df.loc[center_pixel, "Qx"].values**2 + 
				qimage_df.loc[center_pixel, "Qy"].values**2)
		
		qmag = sqrt(qimage_df.loc[center_pixel, "Qz"].values**2 + qxy**2)
		
		self.df.loc["polarization", "unit"] = pol_state_text[pol.state]
			
		self.df.loc["dateStamp", "value"] = image_date
		self.df.loc["timeStamp", "value"] = image_time
		self.df.loc["polarization", "value"] = pol_value_text[pol.state]
		self.df.loc["bottom", "value"] = diffractometer.bottom_angle
		self.df.loc["top", "value"] = diffractometer.top_angle
		self.df.loc["topOffset", "value"] = diffractometer.offset_top
		self.df.loc["flip", "value"] = diffractometer.flip_angle
		self.df.loc["flipOffset", "value"] = diffractometer.offset_flip
		self.df.loc["tempA", "value"] = temperatureA
		self.df.loc["tempB", "value"] = temperatureB
		self.df.loc["qmag", "value"] = qmag
		self.df.loc["qip", "value"] = qxy
		self.df.loc["qop", "value"] = qimage_df.loc[center_pixel, "Qz"].values
		
		# print self.df["values"]
		# self.df["values"] = self.df["values"].astype(float32)
		# print self.df["values"]
		# print self.df
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
# 	def data(self, index, role = Qt.DisplayRole):
# 		if (role == Qt.DisplayRole):
# 			value = super(fitsParamsRightColModel, self).data(index, role)
# 			if ( (self.df.index[index.row()] == "dateStamp")
# 					and (index.column() == self.values_col)
# 					):
# 				print "dateStamp"
# 				# print value.strftime("%A, %B %d, %Y")
# 				print value.strftime("%c")
# 				return value.strftime("%c")
# 				return value.strftime("%A, %B %d, %Y")
# 			if ( (self.df.index[index.row()] == "timeStamp")
# 					and (index.column() == self.values_col)
# 					):
# 				print "timeStamp"
# 				print value.strftime("%H : %M : %S . %f")
# 				return value.strftime("%H : %M : %S . %f")
# 			return value
# 		return None
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
	def data(self, index, role = Qt.DisplayRole):
		if (role == Qt.DisplayRole):
			value = super(fitsParamsRightColModel, self).data(index, role)
			if (self.df.index[index.row()] == "dateStamp"):
				return self.df.iloc[index.row(), self.values_col]
			if (self.df.index[index.row()] == "timeStamp"):
				return self.df.iloc[index.row(), self.values_col]
			return value
		return None

# ----------------------------------------------------------------
# ----------------------------------------------------------------
class qtLabelDelegate(QStyledItemDelegate):
	def __init__(self, parent=None):
		super(QStyledItemDelegate, self).__init__(parent)
	
	def paint (self, painter, option, index):
		return
# 		# item = QLabel(QString(index.data()), self)
# 		# item = QLabel(str(index.data()), self)
# 		item = QLabel(index.data().toString(), self.parent())
# 		item.setDisabled(True)
# 		item.setAutoFillBackground(True)
# 		# item.render(painter)
# 		item.drawContents(painter)
	
	# update sizeHint() ?

# ----------------------------------------------------------------
# ----------------------------------------------------------------
class qtHtmlDelegate(QStyledItemDelegate):
	def __init__(self, parent=None):
		super(QStyledItemDelegate, self).__init__(parent)
	
	def paint(self, painter, option, index):
		options = QStyleOptionViewItemV4(option)
		self.initStyleOption(options, index)
		
# 		print "option.displayAlignment:"
# 		print "\tLeft :", (option.displayAlignment & Qt.AlignLeft)
# 		print "\tRight:", (option.displayAlignment & Qt.AlignRight)
		
		# if (option.displayAlignment & Qt.AlignLeft): print "Left"
		# if (option.displayAlignment & Qt.AlignRight): print "Right"
		
		painter.save()
		
		doc = QTextDocument()
		doc.setHtml(options.text)
		
		options.text = ""
		options.widget.style().drawControl(
			QStyle.CE_ItemViewItem, options, painter)
		
		# Assuming .alignment() & Qt.AlignVCenter
		doc_size = self.sizeHint(option, index)
		height_offset = (options.rect.height() - doc_size.height()) / 2.
# 		print "\n", index.row(), ",", index.column(), ":"
# 		print "options.rect.height():", options.rect.height()
# 		print "doc_size.height():", doc_size.height()
# 		print "height_offset:", height_offset
# 		print "doc_size.width():", doc_size.width()
		height_offset = max(0, height_offset)
		painter.translate(
			options.rect.left(), 
			options.rect.top() + height_offset)
		clip = QRectF(0, 0, options.rect.width(), options.rect.height())
		doc.drawContents(painter, clip)
		
		painter.restore()
	
	def sizeHint(self, option, index):
		options = QStyleOptionViewItemV4(option)
		self.initStyleOption(options, index)
		
		doc = QTextDocument()
		doc.setHtml(options.text)
		# doc.setTextWidth(options.rect.width())	# For multiline text
		return QSize(doc.idealWidth(), doc.size().height())

# ----------------------------------------------------------------
# ----------------------------------------------------------------
class qtFloatDelegate(QStyledItemDelegate):
	def __init__(self, parent=None, decimals=6):
		super(QStyledItemDelegate, self).__init__(parent)
		self.decimals = decimals
	
# 	def paint(self, painter, option, index):
# 		painter.save()
# 		
# 		# value = float(index.data().toPyObject())
# 		value = float(index.data())
# 		# painter.drawText(
# 		# 	option.rect, 
# 		# 	Qt.AlignRight & Qt.AlignVCenter, 
# 		# 	"{0:0.{1:d}f}".format(value, self.decimals))
# 		
# 		# Assuming .alignment() & Qt.AlignRight & Qt.AlignVCenter
# 		doc_size = self.sizeHint(option, index)
# 		height_offset = (option.rect.height() - doc_size.height()) / 2.
# 		print "\n", index.row(), ",", index.column(), ":"
# 		print "option.rect.height():", option.rect.height()
# 		print "doc_size.height():", doc_size.height()
# 		print "height_offset:", height_offset
# 		print "doc_size.width():", doc_size.width()
# 		height_offset = max(0, height_offset)
# 		height_offset = 0
# 		painter.translate(
# 			# option.rect.right() - doc_size.width(), 
# 			option.rect.left(), 
# 			# option.rect.left() + doc_size.width()/2., 
# 			option.rect.top() + height_offset)
# 		painter.drawText(
# 			option.rect, 
# 			# Qt.AlignRight & Qt.AlignVCenter, 
# 			Qt.AlignLeft & Qt.AlignTop, 
# 			"{0:0.{1:d}f}".format(value, self.decimals))
# 		
# 		painter.restore()
	
	def paint(self, painter, option, index):
		options = QStyleOptionViewItemV4(option)
		self.initStyleOption(options, index)
		
		painter.save()
		
		doc = QTextDocument()
		# value = float(index.data().toPyObject())
		value = float(index.data())
		doc.setPlainText("{0:0.{1:d}f}".format(value, self.decimals))
		if isnan(value):
			doc.setPlainText("")
		
		options.text = ""
		options.widget.style().drawControl(
			QStyle.CE_ItemViewItem, options, painter)
		
		# Assuming .alignment() & Qt.AlignRight & Qt.AlignVCenter
		doc_size = self.sizeHint(option, index)
		height_offset = (options.rect.height() - doc_size.height()) / 2.
# 		print "\n", index.row(), ",", index.column(), ":"
# 		print "options.rect.height():", options.rect.height()
# 		print "doc_size.height():", doc_size.height()
# 		print "height_offset:", height_offset
# 		print "doc_size.width():", doc_size.width()
		height_offset = max(0, height_offset)
		painter.translate(
			options.rect.right() - doc_size.width(), 
			options.rect.top() + height_offset)
		clip = QRectF(0, 0, options.rect.width(), options.rect.height())
		doc.drawContents(painter, clip)
		
		painter.restore()
	
	def sizeHint(self, option, index):
		options = QStyleOptionViewItemV4(option)
		self.initStyleOption(options, index)
		# print "index ({0:d}, {1:d}): data =".format(index.row(), index.column()), index.data().toPyObject()
		# print "index ({0:d}, {1:d}): data =".format(index.row(), index.column()), index.data()
		
		doc = QTextDocument()
		# value = float(index.data().toPyObject())
		value = float(index.data())
		doc.setPlainText("{0:0.{1:d}f}".format(value, self.decimals))
		# doc.setTextWidth(options.rect.width())	# For multiline text
		return QSize(doc.idealWidth(), doc.size().height())

# ----------------------------------------------------------------
# ----------------------------------------------------------------
class qtButtonDelegate(QStyledItemDelegate):
	def __init__(self, parent=None, decimals=6):
		super(QStyledItemDelegate, self).__init__(parent)
	
	def paint(self, painter, option, index):
		# options = QStyleOptionViewItemV4(option)
		# self.initStyleOption(options, index)
		
		painter.save()
		
		doc = QPushButton(index.data(), self.parent() )
		
		# options.text = ""
		# options.widget.style().drawControl(
		# 	QStyle.CE_PushButton, options, painter)
		btn_option = QStyleOptionButton()
		# btn_option.initFrom(option)
		# print "btn_option.state:", type(btn_option.state), btn_option.state
		# print "QStyle.State_Enabled:", type(QStyle.State_Enabled), QStyle.State_Enabled
		# print "QStyle.State_Raised:", type(QStyle.State_Raised), QStyle.State_Raised
		print "btn_option.features:", btn_option.features
		# btn_option.features = QStyleOptionButton.None
		# btn_option.features = QStyleOptionButton.Flat
		btn_option.state = QStyle.State_Enabled or QStyle.State_Raised
		btn_option.state = QStyle.State_Raised
		btn_option.rect = option.rect
		btn_option.text = index.data()
		doc.resize(doc.minimumSizeHint())
		
		# Assuming .alignment() & Qt.AlignCenter
		doc_size = self.sizeHint(option, index)
		btn_option.rect = QRect(
			QPoint(option.rect.left(), option.rect.top()), doc_size)
		btn_option.rect = QRect(
			QPoint(option.rect.left()+5, option.rect.top()+5), 
			QSize(doc_size.width()-10, doc_size.height()-10) )
		btn_option.rect = option.rect.adjusted(1, 1, -1, -1)
		btn_option.rect = option.rect.adjusted(2, 2, -2, -2)
		btn_option.rect = option.rect.adjusted(15, 5, -15, -5)
		height_offset = (option.rect.height() - doc_size.height()) / 2.
		width_offset = (option.rect.width() - doc_size.width()) / 2.
		print "\n", index.row(), ",", index.column(), ":"
		print "option.rect.height():", option.rect.height()
		print "doc_size.height():", doc_size.height()
		print "height_offset:", height_offset
		print "doc_size.width():", doc_size.width()
		height_offset = max(0, height_offset)
		width_offset = max(0, width_offset)
# 		painter.translate(
# 			option.rect.left() + width_offset, 
# 			option.rect.top() + height_offset)
# 		clip = QRectF(0, 0, option.rect.width(), option.rect.height())
		# doc.drawContents(painter, clip)
		# doc.style().drawControl(
		QApplication.style().drawControl(
			QStyle.CE_PushButton, btn_option, painter)
		
		painter.restore()
	
	def sizeHint(self, option, index):
		# options = QStyleOptionViewItemV4(option)
		# self.initStyleOption(options, index)
		# print "index ({0:d}, {1:d}): data =".format(index.row(), index.column()), index.data().toPyObject()
		print "index ({0:d}, {1:d}): data =".format(index.row(), index.column()), index.data()
		
		doc = QPushButton(index.data())
		print "doc.sizeHint():", doc.sizeHint()
		print "doc.minimumSizeHint():", doc.minimumSizeHint()
		doc.resize(doc.minimumSizeHint())
		print "doc.size():", doc.size()
		print "doc.rect():", doc.rect().left(), doc.rect().top(), doc.rect().right(), doc.rect().bottom()
		print "doc.contentsRect():", doc.contentsRect().left(), doc.contentsRect().top(), doc.contentsRect().right(), doc.contentsRect().bottom()
		print "doc.contentsMargins():", doc.contentsMargins().left(), doc.contentsMargins().top(), doc.contentsMargins().right(), doc.contentsMargins().bottom()
		# doc.setTextWidth(options.rect.width())	# For multiline text
		# return QSize(doc.idealWidth(), doc.size().height())
		return doc.size()

# ----------------------------------------------------------------
# ----------------------------------------------------------------
class qtDateDelegate(QStyledItemDelegate):
	def __init__(self, parent=None):
		super(QStyledItemDelegate, self).__init__(parent)
		
	def paint(self, painter, option, index):
		options = QStyleOptionViewItemV4(option)
		self.initStyleOption(options, index)
		
		painter.save()
		
		doc = QTextDocument()
		value = index.data()
		try:
			doc.setPlainText(value.strftime("%A, %B %d, %Y"))
		except:
			doc.setPlainText("")
		
		options.text = ""
		options.widget.style().drawControl(
			QStyle.CE_ItemViewItem, options, painter)
		
		# Assuming .alignment() & Qt.AlignLeft & Qt.AlignVCenter
		doc_size = self.sizeHint(option, index)
		height_offset = (options.rect.height() - doc_size.height()) / 2.
# 		print "\n", index.row(), ",", index.column(), ":"
# 		print "options.rect.height():", options.rect.height()
# 		print "doc_size.height():", doc_size.height()
# 		print "height_offset:", height_offset
# 		print "doc_size.width():", doc_size.width()
		height_offset = max(0, height_offset)
		painter.translate(
			# options.rect.right() - doc_size.width(), 
			options.rect.left(), 
			options.rect.top() + height_offset)
		clip = QRectF(0, 0, options.rect.width(), options.rect.height())
		doc.drawContents(painter, clip)
		
		painter.restore()
	
	def sizeHint(self, option, index):
		options = QStyleOptionViewItemV4(option)
		self.initStyleOption(options, index)
		# print "index ({0:d}, {1:d}): data =".format(index.row(), index.column()), index.data().toPyObject()
		# print "index ({0:d}, {1:d}): data =".format(index.row(), index.column()), index.data()
		
		doc = QTextDocument()
		value = index.data()
		try:
			doc.setPlainText(value.strftime("%A, %B %d, %Y"))
		except:
			doc.setPlainText("")
		# doc.setTextWidth(options.rect.width())	# For multiline text
		return QSize(doc.idealWidth(), doc.size().height())

# ----------------------------------------------------------------
# ----------------------------------------------------------------
class qtTimeDelegate(QStyledItemDelegate):
	def __init__(self, parent=None):
		super(QStyledItemDelegate, self).__init__(parent)
		
	def paint(self, painter, option, index):
		options = QStyleOptionViewItemV4(option)
		self.initStyleOption(options, index)
		
		painter.save()
		
		doc = QTextDocument()
		value = index.data()
		try:
			doc.setPlainText("Time stamp: " + value.strftime("%H:%M:%S"))
		except:
			doc.setPlainText("")
		
		options.text = ""
		options.widget.style().drawControl(
			QStyle.CE_ItemViewItem, options, painter)
		
		# Assuming .alignment() & Qt.AlignLeft & Qt.AlignVCenter
		doc_size = self.sizeHint(option, index)
		height_offset = (options.rect.height() - doc_size.height()) / 2.
# 		print "\n", index.row(), ",", index.column(), ":"
# 		print "options.rect.height():", options.rect.height()
# 		print "doc_size.height():", doc_size.height()
# 		print "height_offset:", height_offset
# 		print "doc_size.width():", doc_size.width()
		height_offset = max(0, height_offset)
		painter.translate(
			# options.rect.right() - doc_size.width(), 
			options.rect.left(), 
			options.rect.top() + height_offset)
		clip = QRectF(0, 0, options.rect.width(), options.rect.height())
		doc.drawContents(painter, clip)
		
		painter.restore()
	
	def sizeHint(self, option, index):
		options = QStyleOptionViewItemV4(option)
		self.initStyleOption(options, index)
		# print "index ({0:d}, {1:d}): data =".format(index.row(), index.column()), index.data().toPyObject()
		# print "index ({0:d}, {1:d}): data =".format(index.row(), index.column()), index.data()
		
		doc = QTextDocument()
		value = index.data()
		try:
			doc.setPlainText("Time stamp: " + value.strftime("%H:%M:%S"))
		except:
			doc.setPlainText("")
		# doc.setTextWidth(options.rect.width())	# For multiline text
		return QSize(doc.idealWidth(), doc.size().height())

# ----------------------------------------------------------------
# ----------------------------------------------------------------