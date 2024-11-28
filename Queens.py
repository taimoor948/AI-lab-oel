import tkinter as tk
import random
import time

# Optimized Fitness Function: Directly counting attacking pairs
def fitness(solution):
    n = len(solution)
    attacking_pairs = 0
    for i in range(n):
        for j in range(i + 1, n):
            if solution[i] == solution[j] or abs(solution[i] - solution[j]) == abs(i - j):
                attacking_pairs += 1
    max_pairs = n * (n - 1) // 2
    return max_pairs - attacking_pairs

# Generate initial population
def generate_population(pop_size, n):
    return [[random.randint(0, n - 1) for _ in range(n)] for _ in range(pop_size)]

# Tournament selection
def select_parents(population, fitnesses, tournament_size=5):
    parents = []
    for _ in range(2):
        tournament = random.sample(list(zip(population, fitnesses)), tournament_size)
        parent = max(tournament, key=lambda x: x[1])[0]
        parents.append(parent)
    return parents

# Crossover: Uniform Crossover
def crossover(parent1, parent2):
    child1, child2 = parent1[:], parent2[:]
    for i in range(len(parent1)):
        if random.random() > 0.5:
            child1[i], child2[i] = parent2[i], parent1[i]
    return child1, child2

# Mutation: Randomly change a queen's row in one column
def mutate(solution, mutation_rate):
    if random.random() < mutation_rate:
        col = random.randint(0, len(solution) - 1)
        solution[col] = random.randint(0, len(solution) - 1)
    return solution

# GUI-based Genetic Algorithm
class QueensGA:
    def __init__(self, root, pop_size, n, max_generations, mutation_rate):
        self.root = root
        self.n = n
        self.pop_size = pop_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.cell_size = 60
        self.canvas = tk.Canvas(root, width=n * self.cell_size, height=n * self.cell_size, bg="lightblue")
        self.canvas.pack(pady=10)
        self.generation_label = tk.Label(root, text="Generation: 0", font=("Arial", 16), fg="blue")
        self.generation_label.pack()
        self.status_label = tk.Label(root, text="Status: Running", font=("Arial", 14), fg="green")
        self.status_label.pack()
        self.start_button = tk.Button(root, text="Arrange", command=self.run_ga, font=("Arial", 14), bg="lightgreen")
        self.start_button.pack(pady=5)

    def draw_board(self, solution):
        self.canvas.delete("all")
        for i in range(self.n):
            for j in range(self.n):
                color = "white" if (i + j) % 2 == 0 else "darkgray"
                self.canvas.create_rectangle(
                    j * self.cell_size, i * self.cell_size,
                    (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                    fill=color
                )
        for col, row in enumerate(solution):
            x = col * self.cell_size + self.cell_size // 2
            y = row * self.cell_size + self.cell_size // 2
            self.canvas.create_oval(
                x - 20, y - 20, x + 20, y + 20,
                fill="red", outline="black"
            )

    def run_ga(self):
        population = generate_population(self.pop_size, self.n)
        best_fitness = -1
        stagnant_generations = 0
        
        for generation in range(self.max_generations):
            fitnesses = [fitness(individual) for individual in population]
            max_fitness = max(fitnesses)
            best_solution = population[fitnesses.index(max_fitness)]
            self.generation_label.config(text=f"Generation: {generation + 1}, Best Fitness: {max_fitness}")
            self.draw_board(best_solution)
            self.root.update()
            time.sleep(0.1)

            if max_fitness == self.n * (self.n - 1) // 2:
                self.status_label.config(text="Status: Solution Found!", fg="green")
                print(f"Solution found in generation {generation+1}: {best_solution}")
                return

            # If no improvement in fitness for 20 generations, break
            if max_fitness == best_fitness:
                stagnant_generations += 1
                if stagnant_generations > 20:
                    self.status_label.config(text="Status: Stagnation Detected, Stopping", fg="orange")
                    break
            else:
                stagnant_generations = 0

            best_fitness = max_fitness
            new_population = []
            for _ in range(self.pop_size // 2):
                parent1, parent2 = select_parents(population, fitnesses)
                child1, child2 = crossover(parent1, parent2)
                new_population.extend([mutate(child1, self.mutation_rate), mutate(child2, self.mutation_rate)])
            population = new_population

        self.status_label.config(text="Status: No Solution Found", fg="red")
        print("No perfect solution found.")

# Splash screen
def show_splash():
    splash = tk.Toplevel()
    splash.title("Welcome")
    splash.geometry("400x300")
    splash.configure(bg="lightblue")
    splash_label = tk.Label(
        splash, text="Welcome to the 6-Queens Genetic Algorithm Game!", 
        font=("Arial", 16), fg="blue", bg="lightblue", wraplength=300
    )
    splash_label.pack(expand=True)
    splash.update()
    time.sleep(3)
    splash.destroy()

# Main function
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window while showing the splash screen
    show_splash()
    root.deiconify()  # Show the main window after the splash screen
    root.title("6-Queens Problem - Genetic Algorithm")
    app = QueensGA(root, pop_size=50, n=6, max_generations=300, mutation_rate=0.2)
    root.mainloop()
