using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;

public class FabricCutting
{
    public int FabricWidth = 2000;
    public List<(int width, int height)> Pieces = new List<(int width, int height)>
    {
        (1000, 2000), (1000, 2000), (1000, 2000),
        (660, 2000), (660, 2000), (660, 2000),
        (500, 1000), (500, 1000), (500, 1000), (500, 2000), (300, 500),
        (300, 500), (200, 900)
    };

    public bool IsSpaceFree(List<(int x, int y, int width, int height)> placements, int x, int y, int width, int height, int fabricWidth)
    {
        if (x + width > fabricWidth)
            return false;

        foreach (var (px, py, pwidth, pheight) in placements)
        {
            if (!(x + width <= px || x >= px + pwidth || y + height <= py || y >= py + pheight))
                return false;
        }
        return true;
    }

    public void AppendIfNotExists(List<int> arr, int item)
    {
        if (!arr.Contains(item))
            arr.Add(item);
    }

    public List<(int x, int y, int width, int height)> FillGaps(List<(int x, int y, int width, int height)> placements, List<(int width, int height)> pieces, int fabricWidth)
    {
        var newPlacements = new List<(int x, int y, int width, int height)>(placements);
        pieces = pieces.OrderByDescending(p => p.width * p.height).ToList();
        var yPositions = new List<int> { 0 };
        int maxHeight = 0;

        foreach (var (width, height) in pieces)
        {
            bool placed = false;
            yPositions.Sort();

            foreach (var y in yPositions)
            {
                if (placed)
                    break;
                for (int x = 0; x < fabricWidth; x++)
                {
                    if (IsSpaceFree(newPlacements, x, y, width, height, fabricWidth))
                    {
                        newPlacements.Add((x, y, width, height));
                        AppendIfNotExists(yPositions, y + height);
                        if (maxHeight < y + height)
                            maxHeight = y + height;
                        placed = true;
                        break;
                    }
                }
            }

            if (!placed)
            {
                int currentMaxY = newPlacements.Max(p => p.y + p.height);
                newPlacements.Add((0, currentMaxY, width, height));
                AppendIfNotExists(yPositions, currentMaxY + height);
            }

            for (int i = 0; i < newPlacements.Count; i++)
            {
                for (int j = i + 1; j < newPlacements.Count; j++)
                {
                    var (px1, py1, pw1, ph1) = newPlacements[i];
                    var (px2, py2, pw2, ph2) = newPlacements[j];

                    if (px1 + pw1 <= px2 && IsSpaceFree(newPlacements, px1 + pw1, py1, width, height, fabricWidth))
                    {
                        newPlacements.Add((px1 + pw1, py1, width, height));
                        placed = true;
                        break;
                    }

                    if (py1 + ph1 <= py2 && IsSpaceFree(newPlacements, px1, py1 + ph1, width, height, fabricWidth))
                    {
                        newPlacements.Add((px1, py1 + ph1, width, height));
                        placed = true;
                        break;
                    }
                }
                if (placed)
                    break;
            }
        }

        return newPlacements;
    }

    public void VisualizePlacements(List<(int x, int y, int width, int height)> placements, int fabricWidth)
    {
        Application.Run(new VisualizerForm(placements, fabricWidth));
    }

    public class VisualizerForm : Form
    {
        private List<(int x, int y, int width, int height)> placements;
        private int fabricWidth;

        public VisualizerForm(List<(int x, int y, int width, int height)> placements, int fabricWidth)
        {
            this.placements = placements;
            this.fabricWidth = fabricWidth;
            this.Paint += new PaintEventHandler(DrawPlacements);
            this.Width = fabricWidth / 5;
            this.Height = placements.Max(p => p.y + p.height) / 5 + 50;
        }

        private void DrawPlacements(object sender, PaintEventArgs e)
        {
            Graphics g = e.Graphics;
            foreach (var (x, y, width, height) in placements)
            {
                g.FillRectangle(Brushes.Gray, x / 5, y / 5, width / 5, height / 5);
                g.DrawRectangle(Pens.Black, x / 5, y / 5, width / 5, height / 5);
            }
        }
    }

    public static void Main()
    {
        var fabricCutting = new FabricCutting();
        var placements = new List<(int x, int y, int width, int height)>();
        Console.WriteLine("Placements before filling gaps:");
        Console.WriteLine(string.Join(", ", placements.Select(p => $"({p.x}, {p.y}, {p.width}, {p.height})")));
        
        placements = fabricCutting.FillGaps(placements, fabricCutting.Pieces, fabricCutting.FabricWidth);
        Console.WriteLine("Placements after filling gaps:");
        Console.WriteLine(string.Join(", ", placements.Select(p => $"({p.x}, {p.y}, {p.width}, {p.height})")));

        fabricCutting.VisualizePlacements(placements, fabricCutting.FabricWidth);
    }
}