import math

class DVD:
  def __init__(self, videoData, ytName):
    self.videoData = videoData
    self.numVideos = len(self.videoData)
    self.ytName = ytName

    self.videos = []
    self.chapters = {}
    self.shortTitles = {}
    for video in self.videoData:
      title = video['title']
      self.videos.append(title)
      self.chapters[title] = video['chapters']
      self.shortTitles[title] = video['short title']
    
    self.pages = self.splitPages()

  def splitPages(self):
    pages = []
    numPages = math.ceil(self.numVideos / 6)
    numVideosPerPage = math.ceil(self.numVideos / numPages)

    for page in range(numPages):
      start = (page*numVideosPerPage)
      end = min(start+numVideosPerPage, self.numVideos)

      print("START:",start, "END:",end)
      pages.append(self.videos[start:end])
    return pages

  def randomizer(self):
    return f"        <pre>g5=random({self.numVideos});\n"+"\n".join([f"          if (g5=={i}) jump title {i};" for i in range(1,self.numVideos)]) + "\n        </pre>"

  def buttonLocations(self, pageVideos):
    return [f"""<use x="{52 + (3 - min(3, len(pageVideos) - 3*(n//3))) * 216/2 + (n%3) * 216}" y="{124 + 132*(n//3)}" width="188" height="132" id="button0{n+1}" xlink:href="#s_button0{n+1}"/>""" for n in range(len(pageVideos))]

  def buttonDefs(self, pageVideos):
    return [f"""
          <button id="button0{n+1}" displayVideoFrame="false">
            <action tsi="0" pgci="{n*2-1}"/>
            <filename>frame-text.xml</filename>
            <parameter name="stroke" normal="#ffffff" highlighted="#ff0000" selected="#ffff00"/>
          </button>""" for n in range(len(pageVideos))]

  def buttonSvgs(self, pageVideos):
    return [f"""
              <svg id="s_button0{n+1}">
                <defs>
                  <clipPath id="cp">
                    <rect x="5%" y="5%" width="90%" height="72%" rx="21" id="def_frame"/>
                  </clipPath>
                </defs>
                <use xlink:href="#def_frame" style="fill:#101010;stroke:none;"/>
                <image x="5%" y="5%" width="90%" height="72%" preserveAspectRatio="xmidymid slice" id="image" xlink:href="Thumbnails\\{pageVideos[n]}.jpg" style="clip-path:url(#cp);opacity:1;"/>
                <g id="body_rect" style="fill:none;stroke:#ffffff;">
                  <use id="rect" xlink:href="#def_frame" style="stroke-width:5;"/>
                </g>
                <g id="body_text" style="fill:#000000;fill-opacity:1;stroke:none;">
                  <text x="50%" y="83%" id="text" xml:space="preserve" style="dominant-baseline:text-after-edge;font-family:sans-serif;font-size:18;text-anchor:middle;" transform="translate(0,0)">{self.shortTitles[pageVideos[n]]}</text>
                </g>
              </svg>""" for n in range(len(pageVideos))]

  def menu(self):
    return [f"""
      <!--************** MENU {pageNum+3} **************-->
      <pgc>
        <vob pause="inf">
          <menu videoFormat="NTSC" aspectRatio="2" rememberLastButton="0">
            <svg width="720" height="405">
              <rect width="720" height="405" id="backgroundColour" style="fill:#000000;"/>
              <image width="720" height="405" preserveAspectRatio="none" id="background" xlink:href="HomePage\\ChapterBackground.jpg"/>
              <defs id="defs">
                {"\n".join(self.buttonSvgs(self.pages[pageNum]))}
                <svg id="s_button07" viewBox="-5 -5 110 50">
                  <defs>
                    <filter id="shadowFilter">
                      <feGaussianBlur stdDeviation="2"/>
                    </filter>
                  </defs>
                  <use x="2" y="2" id="shadow" xlink:href="#arrow" style="fill:none;filter:url(#shadowFilter);stroke:#202020;stroke-opacity:1;"/>
                  <g id="main" style="fill:#ffffff;stroke:none;stroke-width:3;">
                    <path id="arrow" style="stroke-width:3;" transform="rotate(180,50,20)" d="M0,10 L50,10 L50,0 L100,20 L50,40 L50,30 L0,30 z"/>
                  </g>
                </svg>
                <svg id="s_button08" viewBox="-5 -5 110 50">
                  <defs>
                    <filter id="shadowFilter">
                      <feGaussianBlur stdDeviation="2"/>
                    </filter>
                  </defs>
                  <use x="2" y="2" id="shadow" xlink:href="#arrow" style="fill:none;filter:url(#shadowFilter);stroke:#202020;stroke-opacity:1;"/>
                  <g id="main" style="fill:#ffffff;stroke:none;stroke-width:3;">
                    <path id="arrow" style="stroke-width:3;" transform="rotate(0,50,20)" d="M0,10 L50,10 L50,0 L100,20 L50,40 L50,30 L0,30 z"/>
                  </g>
                </svg>
              </defs>
              <g id="objects"/>
              <g id="buttons">
                {"\n".join(self.buttonLocations(self.pages[pageNum]))}
                <use x="64" y="36" width="48" height="48" id="button07" xlink:href="#s_button07"/>
                <use x="607" y="36" width="48" height="48" id="button08" xlink:href="#s_button08"/>
              </g>
            </svg>
            {"\n".join(self.buttonDefs(self.pages[pageNum]))}
            <button id="button07">
              <action pgci="{(pageNum * 2) if pageNum != 0 else 0}"/>
              <filename>home-v2.xml</filename>
              <parameter name="fill" normal="#ffffff" highlighted="#ff0000" selected="#ffff00"/>
            </button>
            <button id="button08" autoExecute="true">
              <action pgci="{((pageNum+2) * 2) if (pageNum-1) != len(self.pages) else 0}"/>
              <filename>arrow-simple-v2.xml</filename>
              <parameter name="ac" normal="#ffffff" highlighted="#ff0000" selected="#ffff00"/>
            </button>
          </menu>
        </vob>
      </pgc>""" for pageNum in range(len(self.pages))]

  def vmgm(self):
    return f"""
  <!--************** VMGM **************-->
  <vmgm>
    <menus>
      <video format="ntsc" aspect="16:9" widescreen="nopanscan"/>
      <audio lang="EN"/>
      <subpicture lang="EN"/>
      <!--************** MENU 1 **************-->
      <pgc entry="title">
        <vob pause="inf">
          <audio format="3">HomePage\\Music.mp3</audio>
          <menu videoFormat="NTSC" aspectRatio="2" rememberLastButton="0">
            <svg width="720" height="405">
              <rect width="720" height="405" id="backgroundColour" style="fill:#000000;"/>
              <image width="720" height="405" preserveAspectRatio="xmidymin slice" id="background" xlink:href="HomePage\\Background.jpg"/>
              <defs id="defs">
                <svg id="s_button01">
                  <defs>
                    <filter id="shadowFilter">
                      <feGaussianBlur stdDeviation="3"/>
                    </filter>
                  </defs>
                  <rect x="0" y="0" width="100%" height="100%" rx="5" ry="5" id="background" style="fill:#000000;fill-opacity:0;"/>
                  <use x="2" y="2" id="shadow" xlink:href="#text" style="fill:#404040;fill-opacity:1;filter:url(#shadowFilter);visibility:hidden;"/>
                  <g id="gText" style="fill:#ffffff;">
                    <text x="50%" y="50%" id="text" xml:space="preserve" style="dominant-baseline:middle;font-family:Arial;font-size:28;font-style:normal;font-weight:bold;text-anchor:middle;text-decoration:none;">Play All</text>
                  </g>
                </svg>
                <svg id="s_button02">
                  <defs>
                    <clipPath id="cp">
                      <ellipse cx="50%" cy="50%" rx="45%" ry="45%"/>
                    </clipPath>
                    <filter id="shadowFilter">
                      <feGaussianBlur stdDeviation="3"/>
                    </filter>
                  </defs>
                  <image x="5%" y="5%" width="90%" height="90%" preserveAspectRatio="xmidymid slice" id="image" xlink:href="HomePage\\ChannelPic.jpg" style="clip-path:url(#cp);opacity:1;"/>
                  <use x="2" y="2" id="shadow" xlink:href="#ellipse" style="fill:none;filter:url(#shadowFilter);stroke:#404040;stroke-opacity:1;visibility:hidden;"/>
                  <g id="main" style="fill:none;stroke:#ffffff;">
                    <ellipse cx="50%" cy="50%" rx="45%" ry="45%" id="ellipse" style="fill:none;stroke-width:5;"/>
                  </g>
                </svg>
                <svg id="s_button03">
                  <defs>
                    <filter id="shadowFilter">
                      <feGaussianBlur stdDeviation="3"/>
                    </filter>
                  </defs>
                  <rect x="0" y="0" width="100%" height="100%" rx="5" ry="5" id="background" style="fill:#000000;fill-opacity:0;"/>
                  <use x="2" y="2" id="shadow" xlink:href="#text" style="fill:#404040;fill-opacity:1;filter:url(#shadowFilter);visibility:hidden;"/>
                  <g id="gText" style="fill:#ffffff;">
                    <text x="50%" y="50%" id="text" xml:space="preserve" style="dominant-baseline:middle;font-family:Arial;font-size:28;font-style:normal;font-weight:bold;text-anchor:middle;text-decoration:none;">Random</text>
                  </g>
                </svg>
                <svg id="s_button04" viewBox="0 0 1920 1920">
                  <path id="id01" style="fill:#000000;fill-rule:evenodd;" d="M1264.84,456.279 c31.013,194.462,200.329,343.66,404.01,343.66 c2.516,0,5.03,0,7.545,-0.837 v830.653 c0,92.202,-75.438,167.64,-167.64,167.64 H167.64 c-92.202,0,-167.64,-75.438,-167.64,-167.64 V623.918 c0,-92.201,75.438,-167.64,167.64,-167.64 z M754.378,783.243 h-251.46 c-138.302,0,-251.459,113.157,-251.459,251.46 v167.639 c0,138.302,113.157,251.459,251.46,251.459 h251.459 v-167.64 h-251.46 c-46.1,0,-83.82,-37.719,-83.82,-83.82 v-167.639 c0,-46.1,37.72,-83.82,83.82,-83.82 h251.46 V783.243 z m670.558,0 h-251.46 c-138.302,0,-251.459,113.157,-251.459,251.46 v167.639 c0,138.302,113.157,251.459,251.46,251.459 h251.458 v-167.64 h-251.459 c-46.1,0,-83.82,-37.719,-83.82,-83.82 v-167.639 c0,-46.1,37.72,-83.82,83.82,-83.82 h251.46 V783.243 z M1822.69,121 L1920,219.32 l-157.749,159.342 L1920,538.087 l-97.315,98.237 l-157.748,-159.342 l-157.833,159.342 l-97.315,-98.237 l157.833,-159.425 l-157.833,-159.341 L1507.1,121 l157.833,159.425 L1822.69,121 z"/>
                </svg>
                <svg id="s_button05" viewBox="0 0 1920 1920">
                  <path id="id01" style="fill:#000000;fill-rule:evenodd;" d="M1220.7,478.258 c30.279,186.41,190.667,329.13,385.59,321.259 v803.145 c0,88.346,-72.283,160.63,-160.629,160.63 H160.63 C72.283,1763.29,0,1691.01,0,1602.66 V638.887 c0,-88.346,72.283,-160.629,160.63,-160.629 z m144.647,313.251 h-240.944 c-132.84,0,-240.944,108.104,-240.944,240.944 v160.629 c0,132.84,108.104,240.944,240.944,240.944 h240.944 v-160.63 h-240.944 c-44.253,0,-80.315,-36.06,-80.315,-80.314 v-160.63 c0,-44.252,36.062,-80.314,80.315,-80.314 h240.944 V791.51 z m-642.517,0 H481.887 c-132.84,0,-240.943,108.104,-240.943,240.944 v160.629 c0,132.84,108.103,240.944,240.943,240.944 h240.944 v-160.63 H481.887 c-44.253,0,-80.314,-36.06,-80.314,-80.314 v-160.63 c0,-44.252,36.061,-80.314,80.314,-80.314 h240.944 V791.51 z M1825.87,157 L1920,251.209 l-380.049,380.049 l-246.887,-246.887 l94.21,-94.13 L1539.95,442.92 L1825.87,157 z"/>
                </svg>
              </defs>
              <g id="objects"/>
              <g id="buttons">
                <use x="276" y="312" width="105" height="34" id="button01" xlink:href="#s_button01"/>
                <use x="0" y="124" width="220" height="220" id="button02" xlink:href="#s_button02"/>
                <use x="460" y="312" width="117" height="28" id="button03" xlink:href="#s_button03"/>
                <use x="628" y="328" width="48" height="48" id="button04" xlink:href="#s_button04"/>
                <use x="628" y="276" width="48" height="48" id="button05" xlink:href="#s_button05"/>
              </g>
            </svg>
            <!--PLAY ALL-->
            <button id="button01" defSize="true">
              <action tsi="0" pgci="1" playAll="true"/>
              <filename>text-v3.xml</filename>
              <parameter name="text_fill" normal="#ffffff" highlighted="#0000ff" selected="#ff0000"/>
            </button>
            <!--GO TO CHANNEL-->
            <button id="button02" displayVideoFrame="false">
              <action pgci="4"/>
              <filename>ellipse-v2.xml</filename>
              <parameter name="stroke" normal="#ffffff" highlighted="#0000ff" selected="#ff0000"/>
              <parameter name="fill" normal="none" highlighted="none" selected="none"/>
            </button>
            <!--PLAY RANDOM-->
            <button id="button03" defSize="true">
              <action pgci="2"/>
              <filename>text-v3.xml</filename>
              <parameter name="text_fill" normal="#ffffff" highlighted="#0000ff" selected="#ff0000"/>
            </button>
            <!--CC OFF-->
            <button id="button04">
              <action tsi="0" pgci="1"/>
              <filename>closed-captioning-off.xml</filename>
              <parameter name="param01" normal="#000000" highlighted="#990000" selected="#ee3333"/>
            </button>
            <!--CC ON-->
            <button id="button05">
              <action tsi="0" pgci="1"/>
              <filename>closed-captioning-on.xml</filename>
              <parameter name="param01" normal="#000000" highlighted="#990000" selected="#ee3333"/>
            </button>
          </menu>
        </vob>
      </pgc>
      <!--************** MENU 2 **************-->
      <pgc>
        <vob pause="inf">
          <menu videoFormat="NTSC" aspectRatio="2" rememberLastButton="0">
            <svg width="720" height="405">
              <rect width="720" height="405" id="backgroundColour" style="fill:#000000;"/>
              <defs id="defs"/>
              <g id="objects"/>
              <g id="buttons"/>
            </svg>
          </menu>
        </vob>
        {self.randomizer()}
      </pgc>
      {"\n".join(self.menu())}
    </menus>
  </vmgm>"""

  def titles(self):
    return [f"""      <!--************** TITLE {n+1} = {n*2+1} **************-->
      <pgc>
        <vob file="Videos\\{self.videos[n]}.mp4" chapters="{", ".join(self.chapters[self.videos[n]])}">
          <video format="3"/>
          <audio format="3"/>
          <textsub filename="Subtitles\\{self.videos[n]}.en.srt" characterset="CP1252" fill-color="#ffffffff" outline-color="#000000ff" outline-thickness="3.000000" shadow-color="#000000ff"/>
        </vob>
        <pre>subtitle=g2;</pre>
        <post>call vmgm menu 2;</post>
      </pgc>
""" for n in range(len(self.videos))]

  def styler(self):
    return f"""<?xml version="1.0" encoding="utf-8"?>
  <dvdstyler 
    format="4" 
    xmlns:xlink="http://www.w3.org/1999/xlink"
    template="Basic\\frameTextAutoWS.dvdt"
    isoFile="C:\\Users\\Lenovo\\Videos\\toDVD\\ISOs\\{self.ytName}.iso"
    name="{self.ytName}"
    defPostCommand="2"
    videoFormat="3"
    audioFormat="3"
    aspectRatio="2"
  >
  <colours colour0="#ff0000" colour1="#ffbd00" colour2="#004080"/>
  {self.vmgm()}
  <!--************** TITLESET 1 **************-->
  <titleset>
    <menus>
      <video format="ntsc" aspect="16:9" widescreen="nopanscan"/>
      <audio lang="EN"/>
    </menus>
    <titles>
      <video format="ntsc" aspect="16:9" widescreen="nopanscan"/>
      <audio lang="EN"/>
      <subpicture lang="EN"/>
      {"\n".join(self.titles())}    </titles>
  </titleset>
</dvdstyler>
"""