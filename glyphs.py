import cv2
from glyphfunctions import *
from glyphdatabase import *
 
class Glyphs:
     
    QUADRILATERAL_POINTS = 4
    BLACK_THRESHOLD = 100
    WHITE_THRESHOLD = 155
 
    def detect(self, image):
 
        glyphs = []

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5,5), 0)
        edges = cv2.Canny(gray, 100, 200)

        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
 
        for contour in contours:

            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01*perimeter, True)
 
            if len(approx) == self.QUADRILATERAL_POINTS:

                topdown_quad = get_topdown_quad(gray, approx.reshape(4, 2))

                if topdown_quad[(topdown_quad.shape[0]//100)*5, 
                                (topdown_quad.shape[1]//100)*5] > self.BLACK_THRESHOLD: continue

                glyph_pattern = get_glyph_pattern(topdown_quad, self.BLACK_THRESHOLD, self.WHITE_THRESHOLD)
                glyph_found, _, glyph_name = match_glyph_pattern(glyph_pattern)
 
                if glyph_found:

                    rvecs, tvecs = get_vectors(image, approx.reshape(4, 2))
                    glyphs.append([rvecs, tvecs, glyph_name])
 
        return glyphs