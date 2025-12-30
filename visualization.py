"""
Visualization Module
-------------------
Provides visualization functions for the genetic algorithm results.
"""

import matplotlib.pyplot as plt


def plot_progress(progress, title="Genetic Algorithm Progress", save_path=None):
    """
    Plots the improvement in the best route's distance over generations.
    
    :param progress: List of best distances for each generation.
    :param title: Title for the plot (default: "Genetic Algorithm Progress").
    :param save_path: Optional path to save the plot image. If None, displays the plot.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(progress, linewidth=2)
    plt.ylabel('Distance', fontsize=12)
    plt.xlabel('Generation', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Add annotations for initial and final values
    plt.annotate(f'Initial: {progress[0]:.2f}', 
                xy=(0, progress[0]), 
                xytext=(10, progress[0] + (max(progress) - min(progress)) * 0.1),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                fontsize=10, color='red')
    
    plt.annotate(f'Final: {progress[-1]:.2f}', 
                xy=(len(progress)-1, progress[-1]), 
                xytext=(len(progress)-50, progress[-1] + (max(progress) - min(progress)) * 0.1),
                arrowprops=dict(arrowstyle='->', color='green', lw=1.5),
                fontsize=10, color='green')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_route(route, title="Best Route Found", save_path=None):
    """
    Plots the route on a 2D plane showing the path through all cities.
    
    :param route: List of City objects representing the route.
    :param title: Title for the plot (default: "Best Route Found").
    :param save_path: Optional path to save the plot image. If None, displays the plot.
    """
    plt.figure(figsize=(10, 8))
    
    # Extract coordinates
    x_coords = [city.x for city in route]
    y_coords = [city.y for city in route]
    
    # Close the loop by adding the first city at the end
    x_coords.append(route[0].x)
    y_coords.append(route[0].y)
    
    # Plot the route
    plt.plot(x_coords, y_coords, 'b-', linewidth=2, alpha=0.7, label='Route')
    
    # Plot cities
    plt.scatter(x_coords[:-1], y_coords[:-1], c='red', s=100, zorder=5, 
                edgecolors='black', linewidth=1.5, label='Cities')
    
    # Highlight start/end city
    plt.scatter(route[0].x, route[0].y, c='green', s=200, zorder=6, 
                marker='*', edgecolors='black', linewidth=2, label='Start/End')
    
    plt.xlabel('X Coordinate', fontsize=12)
    plt.ylabel('Y Coordinate', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Route plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_combined(route, progress, save_path=None):
    """
    Creates a combined visualization showing both the route and progress.
    
    :param route: List of City objects representing the best route.
    :param progress: List of best distances for each generation.
    :param save_path: Optional path to save the plot image. If None, displays the plot.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot route on left subplot
    x_coords = [city.x for city in route]
    y_coords = [city.y for city in route]
    x_coords.append(route[0].x)
    y_coords.append(route[0].y)
    
    ax1.plot(x_coords, y_coords, 'b-', linewidth=2, alpha=0.7)
    ax1.scatter(x_coords[:-1], y_coords[:-1], c='red', s=100, zorder=5, 
                edgecolors='black', linewidth=1.5)
    ax1.scatter(route[0].x, route[0].y, c='green', s=200, zorder=6, 
                marker='*', edgecolors='black', linewidth=2)
    ax1.set_xlabel('X Coordinate', fontsize=12)
    ax1.set_ylabel('Y Coordinate', fontsize=12)
    ax1.set_title('Best Route Found', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Plot progress on right subplot
    ax2.plot(progress, linewidth=2, color='purple')
    ax2.set_ylabel('Distance', fontsize=12)
    ax2.set_xlabel('Generation', fontsize=12)
    ax2.set_title('Algorithm Progress', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    improvement = ((progress[0] - progress[-1]) / progress[0]) * 100
    ax2.text(0.5, 0.95, f'Improvement: {improvement:.2f}%', 
            transform=ax2.transAxes, fontsize=11, 
            verticalalignment='top', horizontalalignment='center',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Combined plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()
