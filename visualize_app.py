from bootstrap import Bootstrap
from analyze import Analyze
from visualization import MapVisualization

if __name__ == "__main__":
    main_db = Bootstrap().bootstrap()
    analyzer = Analyze(main_db)
    animals = analyzer.analyze("animals")

    viz = MapVisualization(top_left=(50.00091, 19.92046),
                     bottom_right=(50.00771, 19.89679))
    print(animals)
    viz.draw_map(animals)