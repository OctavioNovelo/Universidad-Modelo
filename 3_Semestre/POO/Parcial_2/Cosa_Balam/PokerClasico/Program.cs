using System.Text;
using PokerClasico;

Console.OutputEncoding = Encoding.UTF8;

// Se agregan las reglas.
IReglasJuego regla = new ReglasPoker();

// Se incia el motor
MotorJuego motor = new MotorJuego(regla);

// Se agrega un jugador con nombre "Jugador 1"
motor.AgregarJugador("Jugador 1");
// Se agrega un jugador pasandole un jugador con nombre y con id
motor.AgregarJugador(new Jugador("Jugador 2", 2));
// Se agrega un jugador con nombre "Jugador 3"
motor.AgregarJugador("Jugador 3");

// Inciar ronda
motor.EjecutarRonda();
