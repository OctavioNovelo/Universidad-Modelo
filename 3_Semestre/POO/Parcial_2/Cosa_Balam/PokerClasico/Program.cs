using System.Text;
using PokerClasico.Modelos;
using PokerClasico.Motor;
using PokerClasico.Reglas;

Console.OutputEncoding = Encoding.UTF8;

IReglasJuego regla = new ReglasPoker();
MotorJuego motor = new MotorJuego(regla);

motor.AgregarJugador("Jugador 1");
motor.AgregarJugador(new Jugador("Jugador 2", 2));
motor.AgregarJugador("Jugador 3");

motor.EjecutarRonda();
