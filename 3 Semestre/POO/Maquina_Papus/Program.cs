namespace MaquinaPapus
{
    internal class Program : CLI
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("////////// Maquina de papus //////////");
            Console.WriteLine("////////////// de papus //////////////");
            Console.WriteLine("///////////// Para papus /////////////"); 
            Console.WriteLine();
            Console.WriteLine();

            Mostrar("help");
            while (true)
            {
                Commmand_Line_Interface();
            }
        }
    }
}
