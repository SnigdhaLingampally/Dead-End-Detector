import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage

def create_start_window():
    clear_window()
    image = tk.PhotoImage(file="C:\\Users\\nebul\\Downloads\\dead-end (3) (3).png")
    image_label = tk.Label(root,image=image,bg="black")
    image_label.image=image
    image_label.place(relwidth=1)
    button_font=("Comic Sans MS",16)
    start_button = tk.Button(root, text="Start", width=25,height=2, command=create_next_window,bg="black",fg="white",font=button_font)
    start_button.pack(side="bottom",anchor="e",padx=200 ,pady=40)
    instruction_button = tk.Button(root, text="Instructions", width=25,height=2, command=instructions,bg="black",fg="white",font=button_font)
    instruction_button.pack(side="bottom",anchor="e",padx=200, pady=40)
def instructions():
    clear_window()
    image = tk.PhotoImage(file="C:\\Users\\nebul\\Downloads\\instructions (1) (4).png")
    image_label = tk.Label(root,image=image,bg="black")
    image_label.image=image
    image_label.place(relwidth=1)
    button_font=("Comic Sans MS",16)
    next_button = tk.Button(root, text="next", width=15,height=1, command=create_next_window,bg="black",fg="white",font=button_font)
    next_button.pack(side="bottom",anchor="e",padx=250 ,pady=40)
    back_button = tk.Button(root, text="back", width=15,height=1, command= create_start_window,bg="black",fg="white",font=button_font)
    back_button.pack(side="bottom",anchor="e",padx=250, pady=40)

def create_next_window():
    clear_window()
    def GraphVisualizer(root,adj_matrix):
        root.title("DEAD-END-DETECTOR")
        canvas = tk.Canvas(root,width=500, height= 400)
        canvas.pack()
        

        node_positions = [
            (200, 150),
            (250, 200),
            (150, 200),
            (100, 150),
            (150, 75),
            (250, 75),
            (400, 50),
            (200, 0)
        ]
        for i in range(len(adj_matrix)):
            for j in range(i, len(adj_matrix[i])):
                if adj_matrix[i][j] == 1:
                    x1, y1 = node_positions[i]
                    x2, y2 = node_positions[j]
                    canvas.create_line(x1, y1, x2, y2)

            x, y = node_positions[i]
            canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="blue")
            canvas.create_text(x,y,text=str(i+1),fill="white",font=("Arial",20))
        num_signs, signs = dead_end_detector(adj_matrix)

        for node in range(len(node_positions)): 
            for sign in signs: 
                if node == sign[0]:
                    x, y = node_positions[node-1]
                    canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="red", width=2)
                    canvas.create_text(x,y,text=str(node),fill="white",font=("Arial",20))

    def adjacency_matrix_to_adjacency_list(adjMatrix):
         n = len(adjMatrix)
         adjList = {}

         for i in range(n):
             for j in range(i, n):
                 if adjMatrix[i][j] == 1:
                     vertex_i = i + 1
                     vertex_j = j + 1

                     if vertex_i not in adjList:
                         adjList[vertex_i] = []
                     if vertex_j not in adjList:
                         adjList[vertex_j] = []

                     adjList[vertex_i].append(vertex_j)
                     adjList[vertex_j].append(vertex_i)

         return adjList

    entry_n = tk.Entry(root)
    entry_m = tk.Entry(root)
    def search_dead_end(loc, graph_dict, visited, dead_ends):
        visited[loc] = True
        neighbours = graph_dict[loc]
        if len(neighbours) == 1:
            dead_ends.append([loc, neighbours[0]])

        for neighbour in neighbours:
            if not visited[neighbour]:
              search_dead_end(neighbour, graph_dict, visited, dead_ends)
   
    def dead_end_detector(adj_matrix):
          graph_dict = adjacency_matrix_to_adjacency_list(adj_matrix)
          dead_ends=[]                                                                                                                       
          visited = {i+1 :False for i in range(len(adj_matrix))}

          for loc in graph_dict:
            if not visited[loc]:
              search_dead_end(loc, graph_dict, visited, dead_ends)

          return len(dead_ends), dead_ends

    label_n = tk.Label(root,text="Enter no.of locations(n):",font=("Times New Roman",16),bg="pink")
    label_n.pack(side="top",padx=50,pady=5)
    entry_n.pack(side="top",padx=100,pady=5)
 
    label_m = tk.Label(root,text="Enter no.of streets(m):",font=("Times New Roman",16),bg="pink")
    label_m.pack(side="top",padx=50,pady=5)    
    entry_m.pack(side="top",padx=100,pady=5)

    entry_streets = []
   
    streets_frame = tk.Frame(root)
    streets_frame.pack(side="top")

    def add_street_entry():
        entry = tk.Entry(streets_frame)
        entry.pack(side="top",padx=100)
        entry_streets.append(entry)
   
    add_streets_button = tk.Button(root, text="Add Streets", command=add_street_entry,bg="yellow",font=("Times New Roman",16))
    add_streets_button.pack(side="top",padx=130,pady=5)

    result_label = tk.Label(root, text="")
    result_label.pack(side="top",padx=50,pady=5)

    signs_label = tk.Label(root, text="")
    signs_label.pack(side="top",padx=50,pady=5)
                                                                         
    def show_result():
        n = int(entry_n.get())
        m = int(entry_m.get())
        streets = []
        adj_matrix = [[0 for i in range(n)] for j in range(n)]

        for i in range(m):
            v, w = map(int, entry_streets[i].get().split())
            streets.append((v, w))
            for i in range(n):
                for j in range(i, n):
                    if v == i+1 and w == j+1:
                        adj_matrix[i][j] = 1
                        adj_matrix[j][i] = 1

        num_signs, signs = dead_end_detector(adj_matrix)
        GraphVisualizer(root,adj_matrix)

        result_label.config(text=f"Number of dead-end signs: {num_signs}",font=("Times New Roman",16))
        signs_label.config(text="Dead-end signs:",font=("Helvetica",16))
        for i, (v, w) in enumerate(signs):
            signs_label.config(text=signs_label.cget("text") + f"\n{v} {w}",font=("Times New Roman",16))

   
    exit_button = tk.Button(root,text="Exit",command=exit_application,font=("Times New Roman",16),bg="lightblue")
    exit_button.pack(side="bottom",padx=140,pady=5)
    detect_button = tk.Button(root, text="Detect Dead-Ends", command=show_result,font=("Times New Roman",16),bg="lightgreen")
    detect_button.pack(side="bottom",padx=80,pady=10)
   
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()
   
def exit_application():
    if messagebox.askyesno("Exit", "Do you want to exit?"):
        root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("DEAD-END-DETECTOR")
    root.geometry("1000x500")

    create_start_window()

root.mainloop()
