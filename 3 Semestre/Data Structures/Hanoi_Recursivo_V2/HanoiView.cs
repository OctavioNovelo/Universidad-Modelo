using System;
using System.Text;
using System.Threading;

namespace StackDev
{
    internal class HanoiView
    {
        // Paleta del programa
        private static readonly ConsoleColor[] PALETA =
        {
            ConsoleColor.Red, ConsoleColor.DarkYellow, ConsoleColor.Yellow, ConsoleColor.Green,
            ConsoleColor.Cyan, ConsoleColor.Blue, ConsoleColor.Magenta, ConsoleColor.DarkMagenta,
            ConsoleColor.DarkGreen, ConsoleColor.DarkCyan
        };

        // Paleta del titulo
        private static readonly ConsoleColor[] PALETA_TITULO =
        {
            ConsoleColor.Red, ConsoleColor.Yellow, ConsoleColor.Green, ConsoleColor.Cyan, ConsoleColor.Magenta
        };

        // Filas del lienzo
        private const int FILA_TITULO = 0;
        private const int FILA_CONTADOR = 1;
        private const int FILA_MENSAJE = 2;
        private const int FILA_CARRIL = 3;   // Aqui va el disco que se esta moviendo
        private const int FILA_POSTE = 4;    
        private const int ANCHO_MIN = 36;    


        // Entre mas movimientos hay, menos detalle se anima (si no, tardaria una eternidad)
        private enum Modo
        {
            Completo,      
            Ligero,        
            Instantaneo    
        }



        // Es como cuando la hacemos en un constructor, no se puede editar despuesn de creada
        private readonly IStack<int>[] torres;
        private readonly int discos;
        private readonly int escala;      // columnas por unidad de ancho de disco (2 = ancho, 1 = angosto, 0 = no cabe: se dibuja a escala)
        private readonly int maxMedia;    // de centro a orilla, lo que mide el disco mas grande
        private readonly int filasDisco;  // filas disponibles para apilar discos (si hay mas discos que filas, varios comparten fila)
        private readonly bool comprimido; // true si el dibujo es "a escala" (no cabe 1 disco por fila o el ancho proporcional)
        private readonly int espacio;      // columnas que ocupa cada torre
        private readonly int ancho;       // ancho total del lienzo
        private readonly int offsetX;     // para centrar las 3 torres dentro del lienzo
        private readonly int filaBase;
        private readonly int filas;
        private readonly int margen;      // para centrar el lienzo en la terminal
        private int origenY;              // fila de la consola donde empieza el lienzo
        private readonly long totalMovs;      // 2^n - 1, pero si no cabe en un long se queda en long.MaxValue (solo se usa para elegir el modo)
        private readonly string textoTotal;   // lo que se muestra en el contador: el numero exacto o "2^n-1" si es enorme
        private readonly Modo modo;
        private readonly int framesDeslizar;
        private readonly int msFrame;
        private readonly int msPausa;



        // Lienzo: una "foto" de la pantalla que se arma en memoria y luego se vuelca a la consola
        private readonly char[,] letra;
        private readonly ConsoleColor[,] fondo;
        private readonly ConsoleColor[,] tinta;
        private readonly string[] anterior;  // para redibujar solo las filas que cambiaron


        private long movimientos;
        private int desfase;                 // gira los colores (lo usa la celebracion final)
        private bool saltar;                 // Ctrl C
        private bool avisarSalto;            // falta dejar en pantalla el aviso "Calculando..." (se hace despues de un Push, cuando el dibujo es coherente)
        private string mensaje = "";
        private ConsoleColor colorMensaje = ConsoleColor.DarkGray;




        // Metodos
        // Esta funciona es para ponerlo en formula por si es muy grande
        public static string TextoTotal(int discos)
        {
            if (discos <= 64)
            {
                return ((1L << discos) - 1).ToString();
            }
            return "2^" + discos + "-1";
        }


        // Devuelve null si la animacion no se puede hacer
        public static HanoiView Crear(IStack<int>[] torres, int discos)
        {
            // Seguridad 
            if (Console.IsOutputRedirected)
            {
                return null;
            }


            // Obtenemos el tamano de la terminal
            int anchoVentana, altoVentana;
            try
            {
                anchoVentana = Console.WindowWidth;
                altoVentana = Console.WindowHeight;
            }
            // Que segun el entorno aveces da una excepcion
            catch (Exception)
            {
                return null;
            }


            // Intentamos primero con discos anchos y si no caben, con discos angostos
            int escala = 0;
            long espacio = 0;
            foreach (int e in new[] { 2, 1 })
            {
                long r = 2L * discos * e + 3;   // L lo convierte a long
                if (Math.Max(3 * r, ANCHO_MIN) <= anchoVentana - 1)
                {
                    escala = e;
                    espacio = r;
                    break;
                }
            }

            int maxMedia;
            if (escala > 0)
            {
                maxMedia = discos * escala;
            }
            else
            {
                espacio = (anchoVentana - 1) / 3;
                if (espacio % 2 == 0)
                {
                    espacio--;   // siempre impar, asi cada torre tiene un centro exacto
                }

                if (espacio < 5 || ANCHO_MIN > anchoVentana - 1)
                {
                    return null;   // si ni asi cabe pues hay que crecer la terminal bro
                }

                maxMedia = (int)(espacio - 3) / 2;
            }

            long filasDisco = Math.Min(discos, (long)altoVentana - FILA_POSTE - 5);
            if (filasDisco < 3)
            {
                return null;
            }

            return new HanoiView(torres, discos, escala, maxMedia, (int)filasDisco, anchoVentana);
        }


        // Constructor
        private HanoiView(IStack<int>[] torres, int discos, int escala, int maxMedia, int filasDisco, int anchoVentana)
        {
            this.torres = torres;
            this.discos = discos;
            this.escala = escala;
            this.maxMedia = maxMedia;
            this.filasDisco = filasDisco;

            comprimido = escala == 0 || filasDisco < discos;
            if (comprimido)
            {
                mensaje = "";
            }

            espacio = 2 * maxMedia + 3;                     // siempre impar, asi cada torre tiene un centro exacto
            ancho = Math.Max(3 * espacio, ANCHO_MIN);
            offsetX = (ancho - 3 * espacio) / 2;
            filaBase = FILA_POSTE + filasDisco + 1;
            filas = filaBase + 2;
            margen = Math.Max(0, (anchoVentana - ancho) / 2);
            // 1L << discos se desborda desde 63 discos, por eso se "topa" en long.MaxValue
            totalMovs = discos >= 63 ? long.MaxValue : (1L << discos) - 1;
            textoTotal = TextoTotal(discos);

            if (totalMovs <= 31)          // hasta 5 discos
            {
                modo = Modo.Completo;
                framesDeslizar = 14;
                msFrame = 15;
                msPausa = 120;
            }
            else if (totalMovs <= 127)    // 6 y 7 discos
            {
                modo = Modo.Ligero;
                framesDeslizar = 5;
                msFrame = 8;
                msPausa = 20;
            }
            else                          // 8 o mas: que dure unos 12 segundos como maximo
            {
                modo = Modo.Instantaneo;
                msPausa = (int)Math.Max(4, Math.Min(80, 12000 / totalMovs));
            }

            letra = new char[filas, ancho];
            fondo = new ConsoleColor[filas, ancho];
            tinta = new ConsoleColor[filas, ancho];
            anterior = new string[filas];
        }

        //******************************************************************
        // Inicio y final
        //******************************************************************

        public void Iniciar()
        {
            Console.CancelKeyPress += RestaurarConsola;   // si hacen Ctrl+C no dejamos el cursor escondido
            Console.CursorVisible = false;
            Console.Clear();
            origenY = Console.CursorTop; // Guarda en la poisicon Y el lugar donde esta el cursos (linea actual) que es basicmanete la parte superior izquierda
            Dibujar(0, 0, 0);
        }

        public void Terminar()
        {
            saltar = false;   // aunque hayan saltado la animacion, mostramos el estado final
            mensaje = "LISTO!";
            colorMensaje = ConsoleColor.Green;
            Dibujar(0, 0, 0);

            // Celebracion: los colores de los discos y del titulo giran un ratito
            for (int i = 0; i < 24; i++)
            {
                desfase++;
                Dibujar(0, 0, 0);
                Thread.Sleep(70);
            }

            Console.ResetColor();
            Console.CursorVisible = true;
            Console.SetCursorPosition(0, Math.Min(origenY + filas + 1, Console.BufferHeight - 1));
            Console.CancelKeyPress -= RestaurarConsola;
        }

        private static void RestaurarConsola(object sender, ConsoleCancelEventArgs e)
        {
            Console.ResetColor();
            Console.CursorVisible = true;
        }

        //******************************************************************
        // Movimiento de un disco (esto es lo que llama Program)
        //******************************************************************

        public void Mover(IStack<int> origen, IStack<int> destino)
        {
            if (saltar)
            {
                destino.Push(origen.Pop());
                movimientos++;
                if (avisarSalto)
                {
                    AvisarSalto();
                }
                return;
            }

            int a = Array.IndexOf(torres, origen);
            int b = Array.IndexOf(torres, destino);

            int disco = origen.Pop();                   // el disco "sale" del poste (los datos reales cambian aqui)
            int filaSale = FilaDeNivel(origen.Size);    // fila donde estaba (Size ya bajo)
            int filaLlega = FilaDeNivel(destino.Size);  // fila donde va a caer

            if (modo != Modo.Instantaneo && !saltar)
            {
                int xa = CentroTorre(a);
                int xb = CentroTorre(b);

                Trasladar(disco, xa, filaSale, FILA_CARRIL);      // subir

                for (int i = 1; i <= framesDeslizar; i++)         // deslizar (arranca y frena suave)
                {
                    double t = (double)i / framesDeslizar;
                    double suave = t * t * (3 - 2 * t);
                    int x = xa + (int)Math.Round((xb - xa) * suave);
                    Dibujar(disco, x, FILA_CARRIL);
                    Pausa(msFrame);
                }

                Trasladar(disco, xb, FILA_CARRIL, filaLlega);     // bajar
            }

            destino.Push(disco);                        // el disco "cae" en el otro poste
            movimientos++;
            if (avisarSalto)
            {
                AvisarSalto();
                return;
            }

            Dibujar(0, 0, 0);
            Pausa(msPausa);
        }

        // Mueve el disco en vertical de una fila a otra
        private void Trasladar(int disco, int x, int desde, int hasta)
        {
            int paso = Math.Sign(hasta - desde);
            if (paso == 0)
            {
                return;
            }

            if (modo == Modo.Ligero)
            {
                Dibujar(disco, x, hasta);
                Pausa(msFrame);
                return;
            }

            for (int fila = desde + paso; fila != hasta + paso; fila += paso)
            {
                Dibujar(disco, x, fila);
                Pausa(msFrame);
            }
        }

        // Mensaje para cuando saltamos la animacion
        private void AvisarSalto()
        {
            avisarSalto = false;
            mensaje = "Calculando el resultado...";
            colorMensaje = ConsoleColor.Yellow;
            saltar = false;   
            Dibujar(0, 0, 0);
            saltar = true;
        }

        // Si se preciona una tecla se detiene el programa
        private void Pausa(int ms)
        {
            if (saltar)
            {
                return;
            }

            try
            {
                if (!Console.IsInputRedirected && Console.KeyAvailable)
                {
                    Console.ReadKey(true);
                    saltar = true;
                    avisarSalto = true;
                    return;
                }
            }
            catch (InvalidOperationException)
            {
                
            }

            if (ms > 0)
            {
                Thread.Sleep(ms);
            }
        }



        //******************************************************************
        // Dibujo
        //******************************************************************
        
        //Seguridad/////////////////////////////////////////////////////////////////////////////////////////////////////
        private int CentroTorre(int i)
        {
            return offsetX + i * espacio + espacio / 2;
        }

        // nivel 0 = el disco de hasta abajo
        // Si hay mas discos que filas, varios niveles comparten fila (la torre se dibuja a escala)
        private int FilaDeNivel(int nivel)
        {
            return filaBase - 1 - (int)((long)nivel * filasDisco / discos);
        }

        // Cuanto mide el disco de centro a orilla: proporcional a su numero, o a escala si no cabe
        private int MediaAncho(int disco)
        {
            if (escala > 0)
            {
                return disco * escala;
            }
            return 1 + (int)((long)(disco - 1) * (maxMedia - 1) / Math.Max(1, discos - 1));
        }
        ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        
        
        
        // disco > 0 significa que hay un disco "en el aire" en la columna x y la fila dada
        private void Dibujar(int disco, int x, int fila)
        {
            if (saltar)
            {
                return;
            }

            Componer(disco, x, fila);
            Volcar();
        }

        // Armamos la imagen en memoria
        private void Componer(int discoActual, int xActual, int filaActual)
        {
            // Construccion del plano
            for (int r = 0; r < filas; r++)
            {
                for (int c = 0; c < ancho; c++)
                {
                    letra[r, c] = ' ';
                    fondo[r, c] = ConsoleColor.Black;
                    tinta[r, c] = ConsoleColor.White;
                }
            }

            // Encabezado
            string titulo = "TORRES DE HANOI";
            int colTitulo = (ancho - titulo.Length) / 2;
            for (int i = 0; i < titulo.Length; i++)
            {
                if (titulo[i] != ' ')
                {
                    Poner(FILA_TITULO, colTitulo + i, titulo[i], ConsoleColor.Black, PALETA_TITULO[(i + desfase) % PALETA_TITULO.Length]);
                }
            }

            Centrar(FILA_CONTADOR, $"Discos: {discos}   Movimientos: {movimientos}/{textoTotal}", ConsoleColor.White);
            Centrar(FILA_MENSAJE, mensaje, colorMensaje);

            // Postes, base y numeros de torre
            for (int i = 0; i < 3; i++)
            {
                for (int r = FILA_POSTE; r < filaBase; r++)
                {
                    Poner(r, CentroTorre(i), ' ', ConsoleColor.Gray, ConsoleColor.Gray);
                }

                Poner(filaBase + 1, CentroTorre(i), (char)('1' + i), ConsoleColor.Black, ConsoleColor.Gray);
            }

            for (int c = offsetX; c < offsetX + 3 * espacio; c++)
            {
                Poner(filaBase, c, ' ', ConsoleColor.DarkGray, ConsoleColor.DarkGray);
            }

            // Discos que estan en cada torre. Se recorre por FILAS (no por discos), asi con miles
            // de discos solo se leen los que se ven. Con un disco por fila, cada fila es su nivel.
            for (int i = 0; i < 3; i++)
            {
                int tam = torres[i].Size;
                if (tam == 0)
                {
                    continue;
                }

                int filasUsadas = (int)((long)(tam - 1) * filasDisco / discos) + 1;
                for (int r = 0; r < filasUsadas; r++)
                {
                    // El nivel mas alto que cae en la fila r (con un disco por fila es simplemente r).
                    // Asi el disco de la cima siempre es el real.
                    long nivel = Math.Min(((long)(r + 1) * discos + filasDisco - 1) / filasDisco - 1, tam - 1);
                    DibujarDisco(torres[i].PeekAt((int)nivel), CentroTorre(i), filaBase - 1 - r);
                }
            }

            // El disco que va en el aire, encima de todo
            if (discoActual > 0)
            {
                DibujarDisco(discoActual, xActual, filaActual);
            }
        }

        private void DibujarDisco(int disco, int cx, int fila)
        {
            ConsoleColor color = PALETA[(int)(((long)disco - 1 + desfase) % PALETA.Length)];
            // Si el disco es color osucuro se poner en blanco el numero y si no se pone negro el numero.
            ConsoleColor texto = Oscuro(color) ? ConsoleColor.White : ConsoleColor.Black;

            int media = MediaAncho(disco);
            for (int c = cx - media; c <= cx + media; c++)
            {
                Poner(fila, c, ' ', color, texto);
            }

            // El numero del disco al centro
            string numero = disco.ToString();
            if (numero.Length > 2 * media + 1)
            {
                return;   //el numero no cabe dentro del disco (pasa en el dibujo a escala)
            }
            int inicio = cx - (numero.Length - 1) / 2;
            for (int i = 0; i < numero.Length; i++)
            {
                Poner(fila, inicio + i, numero[i], color, texto);
            }
        }

        private static bool Oscuro(ConsoleColor c)
        {
            return c == ConsoleColor.Blue || c == ConsoleColor.DarkMagenta || c == ConsoleColor.DarkGreen || c == ConsoleColor.DarkCyan || c == ConsoleColor.DarkRed || c == ConsoleColor.DarkBlue;
        }

        private void Centrar(int fila, string texto, ConsoleColor color)
        {
            int col = Math.Max(0, (ancho - texto.Length) / 2);
            for (int i = 0; i < texto.Length; i++)
            {
                Poner(fila, col + i, texto[i], ConsoleColor.Black, color);
            }
        }

        private void Poner(int fila, int col, char ch, ConsoleColor bg, ConsoleColor fg)
        {
            // seguridad
            if (fila < 0 || fila >= filas || col < 0 || col >= ancho)
            {
                return;
            }

            letra[fila, col] = ch; // Guarda la posicion del caracter para q se escriba. 
            fondo[fila, col] = bg; // Guarda el color de fondo (todo de este mismo caracter).
            tinta[fila, col] = fg; // Guarda el color del caracter. 
        }

        // Pasa la imagen de memoria a la consola. Solo reescribe las filas que cambiaron
        // y agrupa las celdas del mismo color en un solo Write (menos parpadeo, mas rapido).
        // Pasamos de memoria a realidad, gracias chat por. 
        private void Volcar()
        {
            StringBuilder clave = new StringBuilder();
            StringBuilder tramo = new StringBuilder();

            for (int r = 0; r < filas; r++)
            {
                clave.Clear();
                for (int c = 0; c < ancho; c++)
                {
                    clave.Append(letra[r, c]);
                    clave.Append((char)(256 + (int)fondo[r, c] * 16 + (int)tinta[r, c]));
                }

                string k = clave.ToString();
                if (k == anterior[r])
                {
                    continue;   //esta fila no cambio
                }
                anterior[r] = k;

                Console.SetCursorPosition(margen, origenY + r);

                int col = 0;
                while (col < ancho)
                {
                    ConsoleColor bg = fondo[r, col];
                    ConsoleColor fg = tinta[r, col];

                    tramo.Clear();
                    while (col < ancho && fondo[r, col] == bg && tinta[r, col] == fg)
                    {
                        tramo.Append(letra[r, col]);
                        col++;
                    }

                    Console.BackgroundColor = bg;
                    Console.ForegroundColor = fg;
                    Console.Write(tramo.ToString());
                }
            }

            Console.ResetColor();
        }
    }
}
