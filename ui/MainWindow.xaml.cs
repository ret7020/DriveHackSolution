using System;
using System.IO;
using System.Diagnostics;
using System.Collections.Generic;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;
using System.Linq;
using System.Text;
using System.Drawing;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Data;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using Microsoft.Win32;

namespace Main_App_For_4_case
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }


        
        public static void Request(string path,TextBox gek, string filename)
        {
            WebRequest request = WebRequest.Create("http://192.168.0.172:8080/upload");
            request.Method = "POST";

                byte[] byteArray = System.IO.File.ReadAllBytes(path);

                request.ContentType = "image";
                request.ContentLength = byteArray.Length;

                Stream dataStream = request.GetRequestStream();
                dataStream.Write(byteArray, 0, byteArray.Length);
                dataStream.Close();
                WebResponse response = request.GetResponse();
                using (dataStream = response.GetResponseStream())
               {
                StreamReader reader = new StreamReader(dataStream);
                string responseFromServer = reader.ReadToEnd();

                gek.Text += "   " + filename + "  :  " + responseFromServer + "\n";
               }

            response.Close();

        }
        private void mainpanel_DragEnter(object sender, DragEventArgs e)
        {
            if (e.Data.GetDataPresent(DataFormats.FileDrop))
            {
                e.Effects = DragDropEffects.Copy;
                Fer.Content = "Загрузка...";

                mainpanel.Fill= new SolidColorBrush(Color.FromRgb(220,220, 220));
            }
        }

        private void mainpanel_Drop(object sender, DragEventArgs e)
        {

                List<string> paths = new List<string>();
            foreach (string obj in (string[])e.Data.GetData(DataFormats.FileDrop))
            {

                if (Directory.Exists(obj))
                {
                    paths.AddRange(Directory.GetFiles(obj, "*.*", SearchOption.AllDirectories));
                }
                else
                {
                    paths.Add(obj);

                }
            }
                for (int i = 0; i < paths.Count; i++) {
                    string filename = Path.GetFileName(paths[i]);
                    Request(paths[i], gek, filename);
                }
               
                mainpanel.Fill = new SolidColorBrush(Color.FromRgb(245, 245, 245));

                Fer.Content = "Файл выбран";

            
        }

        private void mainpanel_DragLeave(object sender, DragEventArgs e)
        {
            Fer.Content = "Перекиньте файлы сюда";
            mainpanel.Fill = new SolidColorBrush(Color.FromRgb(245, 245, 245));

        }

        private void Output_Click(object sender, RoutedEventArgs e)
        {
            gek.Text = "";
            Fer.Content = "Перекиньте файлы сюда";
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog file = new OpenFileDialog();
            file.Title = "Выберете файл";
            file.InitialDirectory = @"C:\Users\Admin\Documents";
            Nullable<bool> res = file.ShowDialog();
            if(res==true) {
                string filename = Path.GetFileName(file.FileName);
            
                Request(file.FileName, gek, filename);  
            }


            
        }
    }
}
