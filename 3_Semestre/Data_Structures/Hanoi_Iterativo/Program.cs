using System; //Se usa para ocupar de otros codigos
using System.Collections.Generic;
using System.Linq;
using System.Numerics;   //BigInteger: con muchos discos 2^(n-2) ya no cabe en un long
using System.Net.Sockets;
using System.Runtime.ExceptionServices;
using System.Text;
using System.Threading.Tasks;

using static System.Console;   //Para no escribir todo eso, solo para las clases estaticas

namespace StackDev    //Es el apellido de la variable
{
    internal class Program
    {
        static void PrintStackStatus<T>(IStack<T> stack)
        {
            #if DEBUG //Es te if es del procesador de texto
            WriteLine(stack.DataPeek());
            #endif

            if (stack is ArrayStack<T>)
            {
                ArrayStack<T> astack = stack as ArrayStack<T>;
                WriteLine($"C: {astack.Capacity}, S: {stack.Size}, E: {stack.Empty}, F: {stack.Full}");
            }
            else
            {
                WriteLine($"E: {stack.Empty}, F: {stack.Full}");
            }
            
            WriteLine();
        }


        //***********************************************************************
        //***********************************************************************
        //Aviso parroquial para que se vea: Habra mucho texto porque me estoy revolviendo un poco, pero igual es para que lo entienda y se entienda, gracias <3
        //***********************************************************************
        //***********************************************************************


        static HanoiView vista;

        //Mueve el disco de arriba de "origen" a "destino".
        //TODOS los movimientos pasan por aqui para que la animacion los vea
        static void Mover(IStack<int> origen, IStack<int> destino)
        {
            if (vista != null)
            {
                vista.Mover(origen, destino);
            }
            else
            {
                destino.Push(origen.Pop());
            }
        }


        //Movimiento de los 3 discos de arriba
        static void MoverTres(IStack<int> origen, IStack<int> auxiliar, IStack<int> destino)
        {
            // 1) El disco 1 va al destino
            Mover(origen, destino);

            // 2) El disco 2 va al auxiliar
            Mover(origen, auxiliar);

            // 3) El disco 1 va encima del disco 2
            Mover(destino, auxiliar);

            // 4) El disco 3 va al destino
            Mover(origen, destino);

            // 5) El disco 1 va al poste donde NO está el disco 3
            Mover(auxiliar, origen);

            // 6) El disco 2 va encima del disco 3
            Mover(auxiliar, destino);

            // 7) El disco 1 va encima del disco 2
            Mover(origen, destino);
        }



        static void Main(string[] args)
        {
            WriteLine("Torre Hanoi iterativa");
            WriteLine("Ingrese el numero de discos:");

            int discos;
            while (true)
            {
                string entrada = ReadLine();
                if (entrada == null)   //ya no hay mas entrada (Ctrl+D, archivo terminado...): no seguimos preguntando
                {
                    return;
                }

                if (int.TryParse(entrada, out discos) && discos >= 1)
                {
                    break;
                }

                WriteLine("Escribe un numero entero mayor o igual a 1:");
            }

            // No hay limite de discos, pero con n discos hacen falta 2^n - 1 movimientos:
            // se duplican con cada disco que se agrega, asi que avisamos antes de empezar
            if (discos > 20)
            {
                WriteLine($"{discos} discos son {HanoiView.TextoTotal(discos)} movimientos.");
                WriteLine("Continuar? (s/n)");
                string respuesta = ReadLine();
                if (respuesta == null || !respuesta.Trim().StartsWith("s", StringComparison.OrdinalIgnoreCase))
                {
                    return;
                }
            }

            // Creamos las tres torres
            IStack<int> uno = new StaticStack<int>(discos, 1); //origen
            IStack<int> dos = new StaticStack<int>(discos);    //auxiliar/destino  depende
            IStack<int> tres = new StaticStack<int>(discos);   //destino/auxiliar  depende

            //aunque despues creo variables llamadas destino, auxiliar, torreA y torreB,
            //no estoy creando nuevas Stacks
            //solamente estoy usando variables que apuntan a estas tres torres


            // Preparamos la animacion
            vista = HanoiView.Crear(new IStack<int>[] { uno, dos, tres }, discos);
            if (vista == null)
            {
                throw new Exception("Terminal chica");
            }
            else
            {
                vista.Iniciar();
            }


            // Con 1 o 2 discos el patron de bloques no aplica, se mueven a mano
            if (discos == 1)
            {
                Mover(uno, tres);
            }
            else if (discos == 2)
            {
                Mover(uno, dos);
                Mover(uno, tres);
                Mover(dos, tres);
            }

            // Si solamente hay 3 discos los movemos directamente
            else if (discos == 3)
            {
                MoverTres(uno, dos, tres);
            }


            // Si hay mas de 3 discos
            else if (discos > 3)
            {
                IStack<int> bloqueEn; //nos dira donde andan los 3 discos

                // Primero movemos los 3 discos de arriba dependiendo de si la cantidad de discos es par o impar decide que direccion toma
                if (discos % 2 == 0)
                {
                    // Par 1 a 2
                    MoverTres(uno, tres, dos);
                    bloqueEn = dos;
                }
                else
                {
                    // Impar 1 a 3
                    MoverTres(uno, dos, tres);
                    bloqueEn = tres;
                }


                // Cantidad de veces que se mueve el bloque de 3 y el disco grande
                //No estoy contando cada movimiento individual
                //Estoy contando los turnos de mi patron, porque cuando le toca al bloque, MoverTres
                //realiza los siete movimientos necesarios por si solo
                BigInteger totalPasos = BigInteger.Pow(2, discos - 2) - 1; ; //Estamos calculando los movimientos: 2^(n-2)-1


                for (BigInteger paso = 2; paso <= totalPasos; paso++) //Hara todos los movimientos
                {
                    //Si es impar es un movimiento de bloque de 3, si es par es del disco grande, para que sigua el patron
                    if (paso % 2 == 1)//Impar
                    {
                        IStack<int> destino;
                        IStack<int> auxiliar;

                        // Decidimos hacia que torre se mueve el bloque de 3 dependiendo de donde esta
                        if (bloqueEn == uno)
                        {
                            destino = (discos % 2 == 0) ? dos : tres;
                        }
                        else if (bloqueEn == dos)
                        {
                            destino = (discos % 2 == 0) ? tres : uno;
                        }
                        else
                        {
                            destino = (discos % 2 == 0) ? uno : dos;
                        }


                        // La torre auxiliar es la que queda libre donde no hay ni uno
                        if (destino != uno && bloqueEn != uno)
                        {
                            auxiliar = uno;
                        }
                        else if (destino != dos && bloqueEn != dos)
                        {
                            auxiliar = dos;
                        }
                        else
                        {
                            auxiliar = tres;
                        }


                        // Movemos el bloque de 3
                        MoverTres(bloqueEn, auxiliar, destino);

                        // Actualizamos donde esta el bloque de 3
                        bloqueEn = destino;
                    }


                    //Disco grande
                    else //Par
                    {
                        IStack<int> torreA;
                        IStack<int> torreB;


                        // Las dos torres que NO tienen el bloque
                        if (bloqueEn == uno)
                        {
                            torreA = dos;
                            torreB = tres;
                        }
                        else if (bloqueEn == dos)
                        {
                            torreA = uno;
                            torreB = tres;
                        }
                        else
                        {
                            torreA = uno;
                            torreB = dos;
                        }


                        // Movemos el disco que corresponde entre las dos torres, que sea legal
                        if (torreA.Empty)
                        {
                            Mover(torreB, torreA);
                        }
                        else if (torreB.Empty)
                        {
                            Mover(torreA, torreB);
                        }
                        else if (torreA.Peek() < torreB.Peek())
                        {
                            Mover(torreA, torreB);
                        }
                        else
                        {
                            Mover(torreB, torreA);
                        }
                    }
                }
            }


            // Cerramos la animacion y mostramos el resultado
            if (vista != null)
            {
                vista.Terminar();
            }

            WriteLine("\nListo :)");

        }

    }
}


