import sys
import os

#Should add more features in later versions
#Currently not used
defaultOptions = {
    "indent": 4
}

operators = ["==", "=", "+", "-", "/", "%", "^", "*"]

def fixLine(line):
    processedLine = line
    if "==" in line and line.count("=") == 1:
        index = line.index("==")
        line = line[:index] + " == " + line[index + 1:]
        #processedLine = line[:index] + " == " + line[index + 1:]
    if "=" in line:
        index = line.index("=")
        line = line[:index] + " = " + line[index + 1:]
        #processedLine = line[:index] + " = " + line[index + 1:]
    if "+" in line:
        index = line.index("+")
        line = line[:index] + " + " + line[index + 1:]
        #processedLine = line[:index] + " + " + line[index + 1:]
    if "-" in line:
        index = line.index("-")
        line = line[:index] + " - " + line[index + 1:]
        #processedLine = line[:index] + " - " + line[index + 1:]
    if "/" in line:
        index = line.index("/")
        line = line[:index] + " / " + line[index + 1:]
        #processedLine = line[:index] + " / " + line[index + 1:]
    if "^" in line:
        index = line.index("^")
        line = line[:index] + " ^ " + line[index + 1:]
        #processedLine = line[:index] + " ^ " + line[index + 1:]
    if "*" in line:
        index = line.index("*")
        line = line[:index] + " * " + line[index + 1:]
        #processedLine = line[:index] + " * " + line[index + 1:]
    if "%" in line:
        index = line.index("%")
        line = line[:index] + " % " + line[index + 1:]
        #processedLine = line[:index] + " % " + line[index + 1:]
    if "+=" in line:
        index = line.index("+=")
        line = line[:index] + " += " + line[index + 1:]
        #processedLine = line[:index] + " += " + line[index + 1:]
    if "-=" in line:
        index = line.index("-=")
        line = line[:index] + " -= " + line[index + 1:]
        #processedLine = line[:index] + " -= " + line[index + 1:]
    if "/=" in line:
        index = line.index("/=")
        line = line[:index] + " /= " + line[index + 1:]
        #processedLine = line[:index] + " /= " + line[index + 1:]
    if "^=" in line:
        index = line.index("^=")
        line = line[:index] + " ^= " + line[index + 1:]
        #processedLine = line[:index] + " ^= " + line[index + 1:]
    if "*=" in line:
        index = line.index("*=")
        line = line[:index] + " *= " + line[index + 1:]
        #processedLine = line[:index] + " *= " + line[index + 1:]
    if "%=" in line:
        index = line.index("%=")
        line = line[:index] + " %= " + line[index + 1:]
        #processedLine = line[:index] + " %= " + line[index + 1:]
    if ">>" in line:
        index = line.index(">>")
        line = line[:index] + " >> " + line[index + 1:]
    if "<<" in line:
        index = line.index("<<")
        line = line[:index] + " << " + line[index + 1:]
    return line
    
    

def cppIndent(File):
    print "Fixing indent in " + File
    with open(File, 'r') as sourceFile:
        with open(File[:len(File) - 4] + "New.cpp", 'w') as destFile:
            lineCount = 0
            sourceLines = sourceFile.read().splitlines()
            strippedLines = [ sourceLine.strip() for sourceLine in sourceLines ]
            lineStack = []
            currentIndent = 0
            singleIfElseFlag = 0
            for line in strippedLines:
                if line == "":
                    destFile.write(line + '\n')
                elif line.startswith('#'):
                    destFile.write(line + '\n')
                elif line.startswith('{'):
                    lineStack.append(line)
                    destFile.write((currentIndent + singleIfElseFlag) * '\t' + fixLine(line) + '\n')
                    if singleIfElseFlag == 1:
                        singleIfElseFlag = 0
                    currentIndent += 1
                elif line.startswith('}'):
                    if lineStack[len(lineStack) - 1] == '{':
                        lineStack.pop()
                        currentIndent -= 1
                        destFile.write((currentIndent + singleIfElseFlag) * '\t' + fixLine(line) + '\n')
                        if singleIfElseFlag == 1:
                            singleIfElseFlag = 0
                    else:
                        print "Mismatch in number of paranthesis."
                        sys.exit(1)
                elif line.startswith("if") or line.startswith("else"):
                    if strippedLines[lineCount + 1] == '{':
                        pass
                    else:
                        destFile.write((currentIndent + singleIfElseFlag) * '\t' + fixLine(line) + '\n')
                        singleIfElseFlag = 1
                else:
                    destFile.write((currentIndent + singleIfElseFlag) * '\t' + fixLine(line) + '\n')
                    if singleIfElseFlag == 1:
                        singleIfElseFlag = 0
                lineCount += 1
    


def cIndent(File):
    print "Still in development. Feel free \
            to contribute."
    sys.exit(1)
                
                


class MagicIndent:
    """A class to fix indentation in HTML files"""
    def __init__(self, targetDirectory):
        os.chdir(targetDirectory)
        filesPresent = os.listdir(os.getcwd())
        for File in filesPresent:
            if File.endswith('.cpp'):
                cppIndent(File)
            #elif File.endswith('.c'):
                #cIndent(File)
                


if __name__ == '__main__':
    arguments = len(sys.argv)
    if arguments == 1:
        print "Please specify the directory"
        sys.exit(1)
    else:
        targetDirectory = sys.argv[1]
        if arguments > 2:
            if sys.argv[2] == '-i':
                try:
                    defaultOptions['indent'] = sys.argv[3]
                except:
                    print "Specify the size of the indentation"
                    sys.exit(1)
    MagicIndent(targetDirectory)
            

                
