/* Ideas:
-Al momento de añadir el precio del producto agregar el IVA automaticamente (16%).
-Hacerle un hash las contraseñas.
-Hacer que el ID se coloque automaticamente.
*/

/* Correciones

*/
#include "general.hpp"
#include "jsons.hpp"


int main ()
{
    while (true)  
    {
        error = 0;  
        limpiarPantalla();

        do
        {
            limpiarPantalla();
            if(error >= 1)
            {
                cout<<"Informacion incorrecta. Intenta de nuevo.\n";
            }

            usuario = verificarId();
        
            if (usuario.is_null())
            {
                error++;
                cin.ignore(numeric_limits<streamsize>::max(), '\n');
            }

        } while (usuario.is_null());

        nuevoDia();
        
        while (true)
        { 
            archivo = abrirJson();

            if (archivo.is_null())
            { 
               if (regresar_al_menu)
               {
               regresar_al_menu = false;  
               continue;                  
               }   
               else
               {
               break;  // Volver al login
               } 
            }
            mostrarArchivo();
            seleccionarAccion();
            modificarDatos();
        }
    }
}