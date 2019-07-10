using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Painter : MonoBehaviour
{
    public Image image = null;
    Texture2D tex;

    int screenWidth = 0;
    int screenHeight = 0;

    int offsetW = 0;
    int offsetH = 0;

    int lastPointPosX = -1;
    int lastPointPosY = -1;

    private void Awake()
    {
        screenWidth = Screen.width;
        screenHeight = Screen.height;

        offsetW = (screenWidth - 1024) / 2;
        offsetH = (screenHeight - 1024) / 2;

        Init();
    }

    public void Init()
    {
        tex = new Texture2D(128, 128);
        for (int i = 0; i < 128; i++)
        {
            for (int j = 0; j < 128; j++)
            {
                tex.SetPixel(i, j, new Color(1, 1, 1, 1));
            }
        }
        ApplySpr();
    }

    public void ApplySpr()
    {
        tex.Apply();
        Sprite sprite = Sprite.Create(tex, new Rect(0, 0, 128, 128), Vector2.zero);
        image.sprite = sprite;
    }

    bool isMouseDown = false;

    private void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            isMouseDown = true;
            lastPointPosX = -1;
            lastPointPosY = -1;
        }

        if (isMouseDown)
        {
            int mouseX = (int)Input.mousePosition.x;
            int mouseY = (int)Input.mousePosition.y;

            if (mouseX < offsetW || mouseY < offsetH || mouseX > 1024 + offsetW || mouseY > 1024 + offsetH)
            {
                isMouseDown = false;
                return;
            }

            mouseX = (mouseX - offsetW) / 8;
            mouseY = (mouseY - offsetH) / 8;

            for (int i = mouseX - 2; i <= mouseX + 2; i++)
            {
                for (int j = mouseY - 2; j <= mouseY + 2; j++)
                {
                    tex.SetPixel(i, j, new Color(0, 0, 0, 1));
                }
            }

            if(lastPointPosX!=-1&& lastPointPosY!=-1)
            {
                //term
            }

            ApplySpr();

            lastPointPosX = mouseX;
            lastPointPosY = mouseY;
        }

        if (Input.GetMouseButtonUp(0))
        {
            isMouseDown = false;
        }

    }

    public void SaveImage()
    {
        byte[] dataBytes = tex.EncodeToPNG();
        string strSaveFile = Application.dataPath + "/rec_letter.png";
        System.IO.FileStream fs = System.IO.File.Open(strSaveFile, System.IO.FileMode.OpenOrCreate);
        fs.Write(dataBytes, 0, dataBytes.Length);
        fs.Flush();
        fs.Close();
    }

    public byte[] GetImageBytes()
    {
        return tex.EncodeToPNG();
    }
}
