Function CalculateFuelFor(mass)
    CalculateFuelFor = Int(mass / 3) - 2
End Function


Set lines = CreateObject("Scripting.Dictionary")
Set fso = CreateObject("Scripting.FileSystemObject")
fullPath = fso.GetAbsolutePathName(".")
Set file = fso.OpenTextFile (fullPath & "\input.txt", 1)
row = 0
Do Until file.AtEndOfStream
    line = file.Readline
    lines.Add row, line
    row = row + 1
Loop

file.Close

total = 0
For Each line in lines.Items
    mass = CLng(line)
    fuel = CalculateFuelFor(mass)
    While fuel > 0
        total = total + fuel
        fuel = CalculateFuelFor(fuel)        
    Wend 
Next

MsgBox "Fuel required is " & total