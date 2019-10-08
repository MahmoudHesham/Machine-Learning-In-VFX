using System;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;

namespace ML_Backend.Python
{
    public static class Solutions
    {
        public static string ConvertTo64(string ImagePath)
        {
            byte[] ImageArray = System.IO.File.ReadAllBytes(ImagePath);
            string base64 = Convert.ToBase64String(ImageArray);

            return base64;
        }

        public static SuperImage SuperResolution(SuperImage image)
        {
            //python superres.py sham.jpg

            var image_path = Path.Combine(Environment.CurrentDirectory, "Python", "SuperRes", "temp", image.Name);

            byte[] img_bytes = Convert.FromBase64String(image.Base64);
            using (Image jpg_image = Image.FromStream(new MemoryStream(img_bytes)))
            {
                jpg_image.Save(image_path, ImageFormat.Jpeg);  // Or Png
            }

            var superres_file = Path.Combine(Environment.CurrentDirectory, "Python", "SuperRes", "superres.py");

            Process SolutionExecution = new Process();
            SolutionExecution.StartInfo.RedirectStandardOutput = true;
            SolutionExecution.StartInfo.FileName = "python";
            SolutionExecution.StartInfo.Arguments = string.Format("{0} {1}", superres_file, image_path);
            SolutionExecution.Start();

            string ExecutionOutput = SolutionExecution.StandardOutput.ReadToEnd();
            ExecutionOutput = ExecutionOutput.Replace(Environment.NewLine, String.Empty);

            if (File.Exists(ExecutionOutput))
            {
                image.ImagePath = ExecutionOutput;
                image.Base64 = ConvertTo64(ExecutionOutput);
            }

            return image;
        }

    }
}
