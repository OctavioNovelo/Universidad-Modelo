using System.Reflection.Metadata.Ecma335;
using Microsoft.VisualBasic;

namespace MaquinaPapus
{
    internal class CLI
    {
        public Lista<Productos> productos = new Lista<Productos>();
        public Lista<Papu> papus = new Lista<Papu>();
        public Lista<Money> money = new Lista<Money>();

        public string Normalizer(string input)
        {
            if (string.IsNullOrWhiteSpace(input))
                return "";

            return input
                .Trim()
                .ToLower()
                .Replace(" ", "")
                .Replace("ñ", "n")
                .Replace("á", "a")
                .Replace("é", "e")
                .Replace("í", "i")
                .Replace("ó", "o")
                .Replace("ú", "u")
                .Replace("ü", "u");
        }   

        public void Commmand_Line_Interface(string input)
        {
            switch(input)
            {
                case "clear": Console.Clear(); break;
                case "help": Mostrar("help"); break; // Imprimir Comandos
                case "productos": Mostrar("productos"); break; // Mostrar matriz de prodcutos
                case "buy": ; break; // Mostrar CLI del apartado de compra
                default: Console.WriteLine($"Papu: Unknow Command: {input}"); break;  
            }
        }

        public bool Admin_Verif(int password, List<Papu> distribuidores)
        {
            foreach (var item in distribuidores)
            {
                var existente = distribuidores.Find(m => m.Password == password);
                if (existente != null)
                {
                    return true;
                }
                else
                {
                    return false;
                }                  
            }
            throw new Exception("No se que hiciste para llegar aca");
        }

        public void Admin_Command_Line_Interface(bool verif)
        {
            if (verif)
            {
                Console.WriteLine("Correct Password");
                // Quitar dinero de lo que tiene el papu y rellenar la maquina expendedora
                // Agregar dinero sobrante (ganancias) de la maquina expendedora
                string input = Normalizer(Console.ReadLine());
                switch (input)
                {
                    case "clear": Console.Clear(); break;
                    case "exit": ; break; // Salir de papu_CLI
                    case "help": Mostrar("papu_help"); break; // Mostrar comandos
                    case "modprod" : 
                    {
                        Mostrar("productos"); 

                        Console.WriteLine("Que producto quieres modificar ?");
                        string input_2 = Normalizer(Console.ReadLine());

                        Productos encontrado = null;
                        foreach (var p in productos)
                        {
                            if (p.Name == input_2)
                            {
                                encontrado = p;
                                break;
                            }
                            else if (p.Ubi == input_2)
                            {
                                encontrado = p;
                                break;
                            }
                        }
                        break;
                    }
                    case "modmoney": Mostrar("money"); break; // Modificar arreglo de dinero de la maquina
                    case "modpapus": Mostrar("papus"); break; // Modificar arreglo de provedores.
                }
            }
            else
            {
                Console.WriteLine("Incorrect Password");
                return;
            }
        }

        // Todos los comandos mostrar son arreglos.
        public void Mostrar(string input)
        {
            switch (input)
            {
                case "productos":
                    Productos[,] matriz = new Productos[6, 5];
                    foreach (Productos producto in productos)
                    {
                        char columna = producto.Ubi[0];
                        int fila = int.Parse(producto.Ubi[1].ToString());

                        int x = columna - 'A';
                        int y = fila - 1;

                        matriz[y, x] = producto;
                    }

                    // Imprimir la matriz
                    for (int fila = 0; fila < 6; fila++)
                    {
                        for (int columna = 0; columna < 5; columna++)
                        {
                            if (matriz[fila, columna] != null)
                            {
                                Console.Write($"[{matriz[fila, columna]}]\t");
                            }
                            else
                            {
                                Console.Write("[VACIO]\t");
                            }
                        }

                        Console.WriteLine();
                    }

                    break;

                case "papus":
                    for (int i = 0; i < papus.Size(); i++)
                    {
                        Console.WriteLine(papus[i]);
                        Console.WriteLine();
                    }
                    break;

                case "money":
                    for (int i = 0; i < money.Size(); i++)
                    {
                        Console.WriteLine(money[i]);
                        Console.WriteLine();
                    }
                    break;

                case "help":
                    Console.WriteLine("///////// Commands /////////");
                    Console.WriteLine();
                    Console.WriteLine("-- help       Show all commands");
                    Console.WriteLine();
                    Console.WriteLine("-- clear      Clean the shell");
                    Console.WriteLine();
                    Console.WriteLine("-- productos  Show all products");
                    Console.WriteLine();
                    Console.WriteLine("-- buy        Buy a product");
                    Console.WriteLine();
                    Console.WriteLine("///////////////////////////");
                    break;

                case "papu_help":
                    Console.WriteLine("///////// Papu Commands /////////");
                    Console.WriteLine();
                    Console.WriteLine("-- help       Show all commands");
                    Console.WriteLine();
                    Console.WriteLine("-- clear      Clean the shell");
                    Console.WriteLine();
                    Console.WriteLine("-- exit       Exit the Papu shell");
                    Console.WriteLine();
                    Console.WriteLine("-- modprod    Modify the products");
                    Console.WriteLine();
                    Console.WriteLine("-- modmoney   Modify the money");
                    Console.WriteLine();
                    Console.WriteLine("-- modpapus   Modify the papus");
                    Console.WriteLine();
                    Console.WriteLine("-- productos  Show all products");
                    Console.WriteLine();
                    Console.WriteLine("-- buy        Buy a product");
                    Console.WriteLine();
                    Console.WriteLine("///////////////////////////");
                    break;

                default:
                    Console.WriteLine("Comando no reconocido.");
                    break;
            }
        }

        public void Buy()
        {
            // Restar -1 al stock de producto
            // Aumentar el dinero de la maquina
        }

        public void Mod_Prod()
        {
            // Modificar un producto es:
            // Mod Stock
            // Mod Price
            // Mod Ubi
        }

        public void Mod_Papu()
        {
            // Modificar un papu es:
            // Mod su dinero
            // Mod su nombre
            // 
        }
    }
}