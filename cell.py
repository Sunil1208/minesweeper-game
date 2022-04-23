from tkinter import Button, Label, messagebox

import random
import settings
import sys

class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.cell_btn_object = None
        self.is_opened = False
        self.is_mine_candidate = False
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
        btn.bind("<Button-2>", self.right_click_actions)
        btn.bind("<Button-3>", self.middle_click_actions)
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
            text=f"Cells Left:{Cell.cell_count}"
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
        # Cancel left and right click event if cell is already opened:
        # self.cell_btn_object.unbind("<Button-1>")
        # self.cell_btn_object.unbind("<Button-2>")

    def show_mine(self):
        # A logic to interrupt the game and display a message that player lost!
        self.cell_btn_object.configure(bg="red", text='BOOM')
        # ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine', 'Game Over', 0)
        messagebox.showinfo("You clicked on a mine", "Game Over")
        sys.exit()

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
            # Replace the text of the cell count label with the newer count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Cells Left:{Cell.cell_count}"
                )
            # If this was a mine candidate, then for safety we should
            # configure the background color to StystemButtonFace
            if self.is_mine_candidate:
                self.cell_btn_object.configure(bg="SystemButtonFace", text="")
        # Mark the cell as opened (Use it as the last line of this method)
        self.is_opened = True
    
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
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(bg="orange", text="MC")
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(bg="SystemButtonFace", text="")
            self.is_mine_candidate = False
    
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