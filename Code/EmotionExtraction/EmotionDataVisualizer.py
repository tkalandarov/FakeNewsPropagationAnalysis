import matplotlib.pyplot as plt

class EmotionDataVisualizer:
    def __init__(self):
        pass

    def plot_data(self, real_news, fake_news, label_real, label_fake, colour_real, colour_fake):
        # Categories (keys from the dictionaries)
        categories = list(fake_news.keys())

        # Values
        fake_values = list(fake_news.values())
        real_values = list(real_news.values())

        # Set up the bar width and positions
        bar_width = 0.35
        index = range(len(categories))  # [0, 1] for 2 categories

        # Plotting
        fig, ax = plt.subplots()
        bar1 = ax.bar(index, real_values, bar_width, label=label_real, color=colour_real)
        bar2 = ax.bar([i + bar_width for i in index], fake_values, bar_width, label=label_fake, color=colour_fake)

        # Add labels and title
        ax.set_xlabel('Categories')
        ax.set_ylabel('Values')
        ax.set_title('Comparison of Fake and Real Data by Emotion')
        ax.set_xticks([i + bar_width / 2 for i in index])
        ax.set_xticklabels(categories)
        ax.legend()

        # Display the plot
        plt.show()