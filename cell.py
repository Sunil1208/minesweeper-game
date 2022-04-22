from tkinter import Button, Label

import random
import settings

class Cell:
    all = []
    cell_count_label_object = None
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.cell_btn_object = None
        self.x = x
        self.y = y

        # Append the object to the Cell.all list
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=12,
            height=4,
        )
        btn.bind("<Button-1>", self.left_click_actions)
        btn.bind("<Button-2>", self.middle_click_actions)
        btn.bind("<Button-3>", self.right_click_actions)
        self.cell_btn_object = btn

    # static method is used when something needs to be accessed/called only once and not everytime when instantiated
    # static method is just for use case of the class and not fo the use case of the instance
    # We need not to pass self if we don't use an instance method
    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg="black",
            fg="white",
            font=("", 30),
            text=f"Cells Left:{settings.CELL_COUNT}"
        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            # if there are no mines around, show/open all the cell and display the numbers
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()

    def show_mine(self):
        # A logic to interrupt the game and display a message that player lost!
        self.cell_btn_object.configure(bg="black", text='BOOM')

    def show_cell(self):
        self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
    
    #read only property
    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter

    #read only property
    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y -1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]
        cells = [cell for cell in cells if cell]
        return cells


    def get_cell_by_axis(self, x, y):
        # Return a cell object based on the values of x,y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
    
    def right_click_actions(self, event):
        print("right click event is ", event)
        print("I am right clicked")
    
    def middle_click_actions(self, event):
        print("middle click ", event)
        print("I am middle clicked")

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all,settings.MINES_COUNT)
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"