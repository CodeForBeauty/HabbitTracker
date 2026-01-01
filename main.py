from os import path

from tkinter import Tk
from tkinter import ttk

def loadData(fileName) -> dict:
  if not path.isfile(fileName):
    return {}
  file = open(fileName, "r")
  raw = file.read().splitlines()
  file.close()

  output = {}
  for line in raw:
    (habbit, days) = line.split(",")
    output[habbit] = int(days)
  
  return output

def saveData(fileName, data):
  file = open(fileName, "w")
  
  for habbit in data:
    file.write(f"{habbit},{data[habbit]}\n")
  
  file.close()

def main():
  fileName = "data.csv"
  data = loadData(fileName)
  
  root = Tk(className="Habbit tracker")
  frame = ttk.Frame(root, padding = 10, height = 480, width = 600)

  frame.pack()

  labels = []

  containers = []

  def changeData(habbit, idx, change):
    data[habbit] += change
    labels[idx].config(text = f"{habbit}: {data[habbit]}")
  
  def deleteHabbit(habbit, idx):
    data.pop(habbit, None)
    containers[idx].destroy()
  
  def createHabbit(habbit, i):
    container = ttk.Frame(frame)
    containers.append(container)

    label = ttk.Label(container, text = f"{habbit}: {data[habbit]}")
    label.grid(row = 0, column = 0)
    labels.append(label)

    ttk.Button(container, text = "+", 
               command = lambda i=i, habbit=habbit : changeData(habbit, i, +1)
               ).grid(row = 0, column = 1)
    ttk.Button(container, text = "-", 
               command = lambda i=i, habbit=habbit : changeData(habbit, i, -1)
               ).grid(row = 0, column = 2)
    ttk.Button(container, text = "delete", 
               command = lambda i=i, habbit=habbit : deleteHabbit(habbit, i)
               ).grid(row = 0, column = 3)
    
    container.grid(row = i)
  

  for (i, habbit) in enumerate(data):
    createHabbit(habbit, i)

  bottom = ttk.Frame(frame)

  newName = ttk.Entry(bottom)
  newName.grid(column = 0, row = 0)
  
  def addHabbit(name):
    if name and not name in data:
      data[name] = 0
      createHabbit(name, len(containers))

      bottom.grid(row = len(containers) + 1)
  
  ttk.Button(bottom, text = "create",
             command = lambda : addHabbit(newName.get())
             ).grid(column = 2, row = 0)
  
  bottom.grid(row = len(containers))

  root.mainloop()
  saveData(fileName, data)

if __name__ == "__main__":
  main()