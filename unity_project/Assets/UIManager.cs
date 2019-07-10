using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using LitJson;

public class UIManager : MonoBehaviour
{
    public Text letterResultText = null;
    public Text letterPrecentText = null;

    public void OnRecButtonClick()
    {
        byte[] imgBytes = transform.GetComponent<Painter>().GetImageBytes();

        List<IMultipartFormSection> iparams = new List<IMultipartFormSection>();

        iparams.Add(new MultipartFormFileSection("rec_img",imgBytes, "rec_img", "image/png"));

        StartCoroutine(PostUrl("http://192.168.1.191:8080/cgi-bin/MLData/hello.py",iparams,(msg)=> {
            JsonData jd = JsonMapper.ToObject(msg);
            string letter = jd["letter"].ToString();
            string precent = jd["precent"].ToString();
            letterResultText.text = letter;
            letterPrecentText.text = precent;
        }));
    }

    public void OnClearBtnClick()
    {
        transform.GetComponent<Painter>().Init();
        letterResultText.text = "";
        letterPrecentText.text = "";
    }

    public IEnumerator PostUrl(string url, List<IMultipartFormSection> iparams,Action<string> callback)
    {

        byte[] boundary = UnityWebRequest.GenerateBoundary();
        byte[] formSections = UnityWebRequest.SerializeFormSections(iparams, boundary);
        byte[] terminate = Encoding.UTF8.GetBytes(String.Concat("\r\n--", Encoding.UTF8.GetString(boundary), "--"));
        // Make my complete body from the two byte arrays
        byte[] body = new byte[formSections.Length + terminate.Length];

        Buffer.BlockCopy(formSections, 0, body, 0, formSections.Length);
        Buffer.BlockCopy(terminate, 0, body, formSections.Length, terminate.Length);
        // Set the content type - NO QUOTES around the boundary
        string contentType = String.Concat("multipart/form-data; boundary=", Encoding.UTF8.GetString(boundary));

        using (UnityWebRequest request = new UnityWebRequest(url, UnityWebRequest.kHttpVerbPOST))
        {
            UploadHandlerRaw uploadHandlerFile = new UploadHandlerRaw(body);
            request.uploadHandler = (UploadHandler)uploadHandlerFile;
            request.uploadHandler.contentType = contentType;
            request.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            yield return request.Send();
            callback(request.downloadHandler.text);
        }
    }

}
