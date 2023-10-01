from bootstrap import Bootstrap
from analyze import Analyze
from visualization import MapVisualization
from reports import Reports

if __name__ == "__main__":
    main_db = Bootstrap().bootstrap()
    analyzer = Analyze(main_db)
    data = analyzer.analyze("animals")
    '''
    viz = MapVisualization(top_left=(50.00091, 19.87),
                     bottom_right=(50.0091, 20.0),
                     cm=(1.0,1.0,0.3,1.0))
    #viz.draw_map(data)
    viz.draw_map_per_type(data)

    data = analyzer.analyze("animals")
    viz = MapVisualization(top_left=(50.00091, 19.87),
                     bottom_right=(50.0091, 20.0),
                     cm=(0.0,1.0,0.3,1.0))
    viz.draw_map(data)
    '''
    viz = Reports()
    viz.draw_report(data, "calls")

    data = analyzer.analyze("costs")
    viz.draw_report(data, "costs")

