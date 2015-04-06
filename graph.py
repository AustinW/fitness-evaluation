import pygal
from pygal import Config
from pygal.style import LightColorizedStyle

class Graph:

	config = None

	line_chart = None

	def __init__(self):

		self.config = Config()

		self.config.show_legend       = False
		self.config.human_readable    = True
		self.config.fill              = True
		self.config.title             = "World Elite Athlete Rankings" # Should override
		self.config.x_label_rotation  = 90
		self.config.label_font_size   = 12
		self.config.show_dots         = True
		self.config.show_legend       = False
		self.config.tooltip_font_size = 24
		self.config.style             = LightColorizedStyle

		self.line_chart = pygal.Line(self.config)

	def get_line_graph(self, title, y_axis_title, stats):

		self.line_chart.title = title
		self.line_chart.x_labels = [item['athlete']['name'] for item in stats]
		self.line_chart.add(y_axis_title, [item['score'] for item in stats])
		
		return self.line_chart.render()

	def get_line_graph_of_weeks(self, title, y_axis_title, stats):

		self.line_chart.title = title
		self.line_chart.x_labels = [item['week'] for item in stats]
		self.line_chart.add(y_axis_title, [item['result'] for item in stats])

		return self.line_chart.render()