import re # regular expressions
import codecs

def importSubsFromSSA(content):
    content = re.sub('\\\N', ' ', content)
    content = re.sub('{[^}]+}', ' ', content)

    # Search the header of the dialogues (after [Events])
    # Example: Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
    m = re.search('\[Events\]', content, re.U)
    m = re.search('Format: ([^\r\n]+)', content[m.start():])
    header = m.group(1).rsplit(', ')

    # Load the subs
    subs = []
    reg = re.compile('(Dialogue|Comment): ([^\r\n]+)', re.UNICODE)
    start = m.start()
    m = re.search(reg, content[start:])
    while m:
        start += m.end()
        line = m.group(2).rsplit(',')
        if len(line) > len(header):
            for i in range(len(header), len(line)):
                line[len(header)-1] += "," + line[i]
        subs.append(dict([(header[x], line[x]) for x in range(0, len(header))]))
        m = re.search(reg, content[start:])
    return subs

if __name__ == "__main__":
    # Open the SSA File
    #filename = "C:\Users\Thomas\Videos\[EroGaKi-Team]_Solty_Rei_22_DVD.ass"
    #filename = "C:\Users\Thomas\Downloads\\aboo_Mother_Ep4_Check-seiken-preenco.ass"
    #filename = "/home/thomas/Downloads/Ayakashi_02.ass"
    filename= r"/home/thomas/Downloads/[EroGaKi-Team]_Snow_Queen_06_ENDING[gorelease].ass"

    f = codecs.open(filename, "r", "utf-8")
    try:
        content = f.read()
    except UnicodeDecodeError:
        f = codecs.open(filename, "r", "iso-8859-1")
        content = f.read()
    f.close()
    subs = importSubsFromSSA(content)
    # subs are loaded in 'subs'
    # ex: subs[0]['Text']
    for s in subs:
        print s
    print
    print "First sub text: " + subs[0]['Text']
    print "Last sub text:  " + subs[len(subs)-1]['Text']


