from cmu_112_graphics import *
from tkinter import *
import sys
import copy
import math
class SplashScreen(Mode):
    def keyPressed(self, event):
        if event.key=="Space":
            self.app.setActiveMode(self.app.gameMode)
    def redrawAll(self, canvas):
        canvas.create_rectangle(0,0,self.width, self.height)
        canvas.create_text(self.width/2, self.height/2-50, \
            text="For best performance, use full screen. Put mouse in middle of cross to calibrate")
        canvas.create_line(self.width/2, self.height/2-25, self.width/2, self.height/2+25)
        canvas.create_line(self.width/2-25, self.height/2, self.width/2+25, self.height/2)
        canvas.create_text(self.width/2, self.height/2+50, text="Press Space to start")
class GameMode(Mode):
    def appStarted(self):
        self.gx=0
        self.gy=0
        self.gz=0
        self.utheta=0
        self.uphi=0
        self.mousex=self.width/2
        self.mousey=self.height/2
        self.view=math.pi/2
        self.furthest=10000
        Triangle1=Triangle([Point(0, 0, 0), Point(0, 10, 0), Point(10, 10, 0)], "blue", "black")
        Triangle2=Triangle([Point(0, 0, 0), Point(10, 10, 0), Point(10, 0, 0)], "blue", "black")
        Triangle3=Triangle([Point(10, 0, 0), Point(10, 10, 0), Point(10, 10, 10)], "blue", "black")
        Triangle4=Triangle([Point(10, 0, 0), Point(10, 10, 10), Point(10, 0, 10)], "blue", "black")
        Triangle5=Triangle([Point(10, 0, 10), Point(10, 10, 10), Point(0, 10, 10)], "blue", "black")
        Triangle6=Triangle([Point(10, 0, 10), Point(0, 10, 10), Point(0, 0, 10)],"blue", "black")
        Triangle7=Triangle([Point(0, 0, 10), Point(0, 10, 10), Point(0, 10, 0)],"blue", "black")
        Triangle8=Triangle([Point(0, 0, 10), Point(0, 10, 0), Point(0, 0, 0)], "blue", "black")
        Triangle9=Triangle([Point(0, 10, 0), Point(0, 10, 10), Point(10, 10, 10)], "blue", "black")
        Triangle10=Triangle([Point(0, 10, 0), Point(10, 10, 10), Point(10, 10, 0)], "blue", "black")
        Triangle11=Triangle([Point(10, 0, 10), Point(0, 0, 10), Point(0, 0, 0)], "blue", "black")
        Triangle12=Triangle([Point(10, 0, 10), Point(0, 0, 0), Point(10, 0, 0)], "blue", "black")
        List1=[Triangle1, Triangle2, Triangle3, Triangle4, Triangle5, Triangle6,\
            Triangle7, Triangle8, Triangle9, Triangle10, Triangle11, Triangle12]
        Ground=Object([Triangle([Point(-50,0,0), Point(-50, 0, 50), Point(50, 0, 0)], "gray", None),\
                    Triangle([Point(-50, 0, 50), Point(50, 0, 50), Point(50, 0, 0)], "gray", None)])
        self.objects=[Ground, Object(List1)]
        self.lightSource=Light(0, 0, -10)
    def loadObject(self, thing):
        self.objects.add(thing)
    def setLightSource(self, x, y, z):
        self.lightSource.value=(x, y, z)
    def keyPressed(self, event):
        if event.key=="a":
            self.gx-=5
            for object in self.objects:
                object.moveLeft(5)
            if not self.lightSource.fixed:
                self.lightSource.moveWithCamera(-5,0,0)
        elif event.key=="s":
            self.gz-=5
            for object in self.objects:
                object.moveBackward(5)
            if not self.lightSource.fixed:
                self.lightSource.moveWithCamera(0,0,-5)
        elif event.key=="d":
            self.gx+=5
            for object in self.objects:
                object.moveRight(5)
            if not self.lightSource.fixed:
                self.lightSource.moveWithCamera(5,0,0)
        elif event.key=="w":
            self.gz+=5
            for object in self.objects:
                object.moveForward(5)
            if not self.lightSource.fixed:
                self.lightSource.moveWithCamera(0,0,5)
        elif event.key=="Space":
            self.gy+=5
            for object in self.objects:
                object.moveUp(5)
            if not self.lightSource.fixed:
                self.lightSource.moveWithCamera(0,5,0)
        elif event.key=="k":
            self.gy-=5
            for object in self.objects:
                object.moveDown(5)
            if not self.lightSource.fixed:
                self.lightSource.moveWithCamera(0,-5,0)
        elif event.key=="f":
            self.lightSource.toggleFixed()
        elif event.key=="m":
            self.lightSource.moveToCamera(self.gx, self.gy, self.gz)
        elif event.key=="r":
            self.setLightSource(0,0,-5)
    def mouseMoved(self, event):
        x, y=self.width/2, self.height/2
        xScale, yScale=360/self.width, 180/self.height
        self.utheta+=(event.x-self.mousex)*xScale
        self.uphi+=(self.mousey-event.y)*yScale
        if event.x<self.mousex:
            for object in self.objects:
                object.rotateLeft((self.mousex-event.x)*xScale)
        else:
            for object in self.objects:
                object.rotateRight((event.x-self.mousex)*xScale)
        if event.y<self.mousey:
            for object in self.objects:
                object.rotateUp((self.mousey-event.y)*yScale)
        else:
            for object in self.objects:
                object.rotateDown((event.y-self.mousey)*yScale)
        self.mousex=event.x
        self.mousey=event.y


    def redrawAll(self, canvas):
        for object in self.objects:
            object.draw(self, canvas)
        canvas.create_text(self.width-50, self.height-20, text=f"({self.gx}, {self.gy}, {self.gz})")
        canvas.create_text(25, self.height-20, text=f"({self.utheta}, {self.uphi})")
        if self.lightSource.fixed:
            string="Static"
        else:
            string="Dynamic"
        canvas.create_text(75, 50, text=f"{string}")
class Object():
    def __init__(self, Triangles):
        self.Triangles=Triangles
        self.appTriangles=self.copyTriangles()
    def copyTriangles(self):
        L=[]
        for tri in self.Triangles:
            P=[]
            for pt in tri.pts:
                x, y, z=pt.value
                P+=[Point(x, y, z)]
            L+=[Triangle(P, tri.fill, tri.outline)]
        return L
    def moveLeft(self, amt):
        for i in self.appTriangles:
            i.moveLeft(amt)
    def moveRight(self, amt):
        for i in self.appTriangles:
            i.moveRight(amt)
    def moveUp(self, amt):
        for i in self.appTriangles:
            i.moveUp(amt)
    def moveDown(self, amt):
        for i in self.appTriangles:
            i.moveDown(amt)
    def moveForward(self, amt):
        for i in self.appTriangles:
            i.moveForward(amt)
    def moveBackward(self, amt):
        for i in self.appTriangles:
            i.moveBackward(amt)
    def rotateLeft(self, amt):
        for i in self.appTriangles:
            i.rotateLeft(amt)
    def rotateRight(self, amt):
        for i in self.appTriangles:
            i.rotateRight(amt)
    def rotateUp(self, amt):
        for i in self.appTriangles:
            i.rotateUp(amt)
    def rotateDown(self, amt):
        for i in self.appTriangles:
            i.rotateDown(amt)
    def draw(self, mode, canvas):
        for i in range(len(self.appTriangles)):
            tri=self.appTriangles[i]
            if tri.show:
                tri.draw(canvas, mode, self.Triangles[i])
class Triangle():
    def __init__(self, pts, fill, outline):
        self.pts=pts
        self.theta=0
        self.phi=0
        self.fill=fill
        self.outline=outline
        self.normal=self.orientation()
        self.show=self.showShape()
    def findShade(self):
        fill=self.fill
        normal=self.normal
    def showShape(self):
        x, y, z=self.normal
        px, py, pz=self.pts[0].value
        dot=x*px+y*py+z*pz
        return (dot<0)
    def moveLeft(self, amt):
        for pt in self.pts:
            pt.updateX(amt)
        self.normal=self.orientation()
        self.show=self.showShape()
    def moveRight(self, amt):
        for pt in self.pts:
            pt.updateX(-1*amt)
        self.normal=self.orientation()
        self.show=self.showShape()
    def moveForward(self, amt):
        for pt in self.pts:
            pt.updateZ(-1*amt)
        self.normal=self.orientation()
        self.show=self.showShape()
    def moveBackward(self, amt):
        for pt in self.pts:
            pt.updateZ(amt)
        self.normal=self.orientation()
        self.show=self.showShape()
    def moveUp(self, amt):
        for pt in self.pts:
            pt.updateY(amt*-1)
        self.normal=self.orientation()
        self.show=self.showShape()
    def moveDown(self, amt):
        for pt in self.pts:
            pt.updateY(amt)
        self.normal=self.orientation()
        self.show=self.showShape()
    def rotateLeft(self, amt):
        for pt in self.pts:
            pt.updateXZ(amt)
        self.normal=self.orientation()
        self.show=self.showShape()
    def rotateRight(self, amt):
        for pt in self.pts:
            pt.updateXZ(-1*amt)
        self.normal=self.orientation()
        self.show=self.showShape()
    def rotateUp(self, amt):
        for pt in self.pts:
            pt.updateYZ(-1*amt)
        self.normal=self.orientation()
        self.show=self.showShape()
    def rotateDown(self, amt):
        for pt in self.pts:
            pt.updateYZ(amt)
        self.normal=self.orientation()
        self.show=self.showShape()
    def orientation(self):
        x0, y0, z0=self.pts[0].value
        x1, y1, z1=self.pts[1].value
        x2, y2, z2=self.pts[2].value
        vx1, vy1, vz1=x1-x0, y1-y0, z1-z0
        vx2, vy2, vz2=x2-x1, y2-y1, z2-z1
        nx=vy1*vz2-vy2*vz1
        ny=vz1*vx2-vz2*vx1
        nz=vx1*vy2-vx2*vy1
        d=math.sqrt(nx**2+ny**2+nz**2)
        return nx/d, ny/d, nz/d
    def draw(self, canvas, mode, tri):
        x0, y0, z0=self.pts[0].value
        x1, y1, z1=self.pts[1].value
        x2, y2, z2=self.pts[2].value
        fill=mode.lightSource.calculateFill(self.fill, tri.normal, tri.pts, canvas)
        if (z0>0.1 and z1>0.1 and z2>0.1):
            w0, h0=self.pts[0].calcPts(canvas, mode)
            w1, h1=self.pts[1].calcPts(canvas, mode)
            w2, h2=self.pts[2].calcPts(canvas, mode)
            canvas.create_polygon(w0, h0, w1, h1,w2, h2, \
                fill=fill, outline=self.outline)
        elif (z0<=0.1 and z1<=0.1 and z2<=0.1):
            pass
        elif (z0>0.1 and z1<=0.1 and z2<=0.1):
            w0, h0=self.pts[0].calcPts(canvas, mode)
            dx, dy, dz=x1-x0, y1-y0, z1-z0
            pt1=Point(x0+dx*(0.1-z0)/dz, y0+dy*(0.1-z0)/dz, 0.1)
            ddx, ddy, ddz=x2-x0, y2-y0, z2-z0
            pt2=Point(x0+ddx*(0.1-z0)/ddz, y0+ddy*(0.1-z0)/ddz, 0.1)
            w1, h1=pt1.calcPts(canvas, mode)
            w2, h2=pt2.calcPts(canvas, mode)
            canvas.create_polygon(w0, h0, w1, h1, w2, h2, \
                fill=fill, outline=self.outline)
        elif (z1>0.1 and z0<=0.1 and z2<=0.1):
            w1, h1=self.pts[1].calcPts(canvas, mode)
            dx, dy, dz=x0-x1, y0-y1, z0-z1
            pt1=Point(x1+dx*(0.1-z1)/dz, y1+dy*(0.1-z1)/dz, 0.1)
            ddx, ddy, ddz=x2-x1, y2-y1, z2-z1
            pt2=Point(x1+ddx*(0.1-z1)/ddz, y1+ddy*(0.1-z1)/ddz, 0.1)
            w0, h0=pt1.calcPts(canvas, mode)
            w2, h2=pt2.calcPts(canvas, mode)
            canvas.create_polygon(w0, h0, w1, h1,w2, h2, \
                fill=fill, outline=self.outline)
        elif (z2>0.1 and z1<=0.1 and z0<=0.1):
            w2, h2=self.pts[2].calcPts(canvas, mode)
            dx, dy, dz=x1-x2, y1-y2, z1-z2
            pt1=Point(x2+dx*(0.1-z2)/dz, y2+dy*(0.1-z2)/dz, 0.1)
            ddx, ddy, ddz=x0-x2, y0-y2, z0-z2
            pt2=Point(x2+ddx*(0.1-z2)/ddz, y2+ddy*(0.1-z2)/ddz, 0.1)
            w1, h1=pt1.calcPts(canvas, mode)
            w0, h0=pt2.calcPts(canvas, mode)
            canvas.create_polygon(w0, h0, w1, h1,w2, h2, \
                fill=fill, outline=self.outline)
        elif (z0<=0.1):
            w1, h1=self.pts[1].calcPts(canvas, mode)
            w2, h2=self.pts[2].calcPts(canvas, mode)
            d1x, d1y, d1z=x0-x1, y0-y1, z0-z1
            pt1=Point(x1+d1x*(0.1-z1)/d1z, y1+d1y*(0.1-z1)/d1z, 0.1)
            d2x, d2y, d2z=x0-x2, y0-y2, z0-z2
            pt2=Point(x2+d2x*(0.1-z2)/d2z, y2+d2y*(0.1-z2)/d2z, 0.1)
            w10, h10=pt1.calcPts(canvas, mode)
            w20, h20=pt2.calcPts(canvas, mode)
            canvas.create_polygon(w1, h1, w2, h2, w10, h10, \
                fill="yellow", outline="blue")
            canvas.create_polygon(w1, h1, w20, h20, w10, h10, fill="blue", outline="yellow")
        elif (z1<=0.1):
            w0, h0=self.pts[0].calcPts(canvas, mode)
            w2, h2=self.pts[2].calcPts(canvas, mode)
            d1x, d1y, d1z=x1-x0, y1-y0, z1-z0
            pt1=Point(x0+d1x*(0.1-z0)/d1z, y0+d1y*(0.1-z0)/d1z, 0.1)
            d2x, d2y, d2z=x1-x2, y1-y2, z1-z2
            pt2=Point(x2+d2x*(0.1-z2)/d2z, y2+d2y*(0.1-z2)/d2z, 0.1)
            w10, h10=pt1.calcPts(canvas, mode)
            w20, h20=pt2.calcPts(canvas, mode)
            canvas.create_polygon(w2, h2, w0, h0, w20, h20, \
                fill=fill, outline="white")
            canvas.create_polygon(w2, h2, w0, h0, w10, h10, fill=fill, outline="orange")
        elif (z2<=0.1):
            w0, h0=self.pts[0].calcPts(canvas, mode)
            w1, h1=self.pts[1].calcPts(canvas, mode)
            d1x, d1y, d1z=x2-x0, y2-y0, z2-z0
            pt1=Point(x0+d1x*(0.1-z0)/d1z, y0+d1y*(0.1-z0)/d1z, 0.1)
            d2x, d2y, d2z=x2-x1, y2-y1, z2-z1
            pt2=Point(x1+d2x*(0.1-z1)/d2z, y1+d2y*(0.1-z1)/d2z, 0.1)
            w10, h10=pt1.calcPts(canvas, mode)
            w20, h20=pt2.calcPts(canvas, mode)
            canvas.create_polygon(w0, h0, w1, h1, w20, h20, fill=fill, outline="red")
            canvas.create_polygon(w0, h0, w1, h1, w10, h10, fill=fill, outline="green")
        else:
            Exception("Cases nonexhuastive")

class Point():
    def __init__(self, x, y, z):
        self.value=(x, y, z)
    def updateX(self, amt):
        x, y, z=self.value
        self.value=(x+amt, y, z)
    def updateY(self, amt):
        x, y, z=self.value
        self.value=(x, y+amt, z)
    def updateZ(self, amt):
        x, y, z=self.value
        self.value=(x, y, z+amt)
    def updateXZ(self, amt):
        x, y, z=self.value
        ramt=math.radians(amt)
        self.value=x*math.cos(ramt)-z*math.sin(ramt), y, x*math.sin(ramt)+z*math.cos(ramt)
    def updateYZ(self, amt):
        x, y, z=self.value
        ramt=math.radians(amt)
        self.value=x, z*math.sin(ramt)+y*math.cos(ramt), z*math.cos(ramt)-y*math.sin(ramt)
    def calcPts(self, canvas, mode):
        x, y, z=self.value
        cx=mode.width/2
        cy=mode.height/2
        if (z<=0):
            px, py, pz=0, 0, 0
        else:
            f=1/(math.tan(mode.view/2))
            q=mode.furthest/(mode.furthest-0.1)
            px, py, pz=f*x*mode.height/(z*mode.width), f*y/(z), z*q-(0.1*q)
        px, py, pz=px+1, py+1, pz+1
        return px*cx, mode.height-py*cy
class Light():
    def __init__(self, x, y, z):
        self.value=(x, y, z)
        self.fixed=True
        self.intensity=75
    def setIntensity(self, lvl):
        assert(0<=lvl and lvl<=100)
        self.intensity=lvl
    def toggleFixed(self):
        self.fixed=(not self.fixed)
    def moveToCamera(self, x, y, z):
        self.value=(x, y, z)
    def moveWithCamera(self, x, y, z):
        x0, y0, z0=self.value
        self.value=x0+x, y0+y, z0+z
    def calculateFill(self, default, normal, pts, canvas):
        if default[0]!="#":
            rgb = canvas.winfo_rgb(default)
            red, green, blue = rgb[0]//256, rgb[1]//256, rgb[2]//256
        else:
            rgb=default[1:]
            red, green, blue= int(rgb[0:2], 16), int(rgb[2:4], 16), int(rgb[4:6], 16)
        for pt in pts:
            x, y, z=pt.value
            lx, ly, lz=self.value
            vx, vy, vz=x-lx, y-ly, z-lz
            norm=math.sqrt(vx**2+vy**2+vz**2)
            if norm!=0:
                break
        ux, uy, uz=vx/norm, vy/norm, vz/norm
        nx, ny, nz=normal
        dot=ux*nx+uy*ny+uz*nz
        lvl=self.intensity*256/100
        nr, ng, nb=int(red-(dot+1)*lvl), int(green-(dot+1)*lvl), int(blue-(dot+1)*lvl)
        if 0>nr:
            nr=0
        if 0>ng:
            ng=0
        if 0>nb:
            nb=0
        if nr>=256:
            nr=255
        if ng>=256:
            ng=255
        if nb>=256:
            nb=255
        return self.rgbString(nr, ng, nb)
    def rgbString(self, red, green, blue):
        return "#%02x%02x%02x" % (red, green, blue)


class EngineApp(ModalApp):
    def appStarted(self):
        self.splashScreenMode = SplashScreen()
        self.gameMode = GameMode()
        self.setActiveMode(self.splashScreenMode)
app = EngineApp(width=500, height=500)
