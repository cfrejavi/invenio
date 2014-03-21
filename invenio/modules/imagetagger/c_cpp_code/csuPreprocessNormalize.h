/*
 *  csuFace2Norm.c
 *  csuFace2Norm
 *
 *  Created by David  Bolme on Sun Jun 09 2002.
 *
 */

/*
Copyright (c) 2003 Colorado State University

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom
the Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
*/
#ifndef PREPROCESS_H
#define PREPROCESS_H
#include <csuCommon.h>

//normalizes images described in the eyeFile, along with the eyes coordinates
//writes the images in sfiDir
void normalizeImages(char* eyeFile, char* inputDir, char* sfiDir);
//do the same as the previous function but for 1 photo and coordinates passed as parameters
void normalizeImageAndWrite(char* imagePath, char* outputPath, double eyelx, double eyely, double eyerx, double eyery, int type);
//normalization without file writting
Image * getRawImages(char* eyeFile, char* inputDir, char* sfiDir, int n);
int getWidth(Image* images, int img);
int getHeight(Image* images, int img);
int getChannels(Image* images, int img);
double getData(Image* images, int img, int col, int row, int channel);
#endif
