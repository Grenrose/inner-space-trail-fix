/* Ask Wine for exactly the font Inner Space uses for icon labels and report
 * what it actually delivers:
 *   CreateFont(7, 0,0,0, 0, 0,0,0, ANSI, 0,0, PROOF_QUALITY,
 *              VARIABLE_PITCH|FF_SWISS, "Small Fonts")
 * The game draws the label at y=32 and only keeps rows 32-37 clean, so any
 * face taller than ~7 px (with blank descender rows) spills into the margin. */
#include <windows.h>
#include <stdio.h>

int main(void)
{
    HDC dc = CreateCompatibleDC(NULL);
    HFONT f = CreateFontA(7, 0, 0, 0, 0, 0, 0, 0, ANSI_CHARSET, 0, 0,
                          PROOF_QUALITY, VARIABLE_PITCH | FF_SWISS, "Small Fonts");
    HGDIOBJ old = SelectObject(dc, f);
    TEXTMETRICA tm;
    char face[64] = "";
    SIZE sz;
    GetTextMetricsA(dc, &tm);
    GetTextFaceA(dc, sizeof(face), face);
    GetTextExtentPoint32A(dc, "CALENDAR", 8, &sz);
    printf("requested: Small Fonts, height 7\n");
    printf("got face : %s  (%s)\n", face,
           (tm.tmPitchAndFamily & TMPF_TRUETYPE) ? "TrueType" :
           (tm.tmPitchAndFamily & TMPF_VECTOR) ? "vector" : "bitmap");
    printf("height %ld  ascent %ld  descent %ld  internal leading %ld\n",
           tm.tmHeight, tm.tmAscent, tm.tmDescent, tm.tmInternalLeading);
    printf("\"CALENDAR\" extent: %ld x %ld px\n", sz.cx, sz.cy);
    printf("label at y=32 occupies rows 32..%ld (cell ends at row 37)\n", 32 + tm.tmHeight - 1);
    SelectObject(dc, old);
    DeleteObject(f);
    DeleteDC(dc);
    return 0;
}
