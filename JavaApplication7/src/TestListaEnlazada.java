

import Laboratorio_Semana07.modelo.*;
import Laboratorio_Semana07.vista.VistaTareasFormulario;
import Laboratorio_Semana07.controlador.ControladorTareas;

import javax.swing.*;
import java.awt.*;
import java.util.LinkedHashMap;
import java.util.Map;

public class TestListaEnlazada {

    public static void main(String[] args) {
        Map<String, Boolean> resultados = new LinkedHashMap<>();
        ListaEnlazadaTareas lista = new ListaEnlazadaTareas();

        System.out.println("=== INICIO DE PRUEBAS ===");

        // PRUEBAS LÓGICA
        resultados.put("agregarAlInicio()", testAgregarAlInicio(lista));
        resultados.put("agregarAlFinal()", testAgregarAlFinal(lista));
        resultados.put("contiene()", testContiene(lista));
        resultados.put("eliminar()", testEliminar(lista));
        resultados.put("imprimir()", testImprimir(lista));
        resultados.put("buscarIndice()", testBuscarIndice(lista));
        resultados.put("actualizarEstado()", testActualizarEstado(lista));

        // PRUEBA DE FORMULARIO
        resultados.put("Formulario Swing", testFormulario());

        // RESULTADOS
        System.out.println("\n=== RESULTADOS ===");
        for (Map.Entry<String, Boolean> r : resultados.entrySet()) {
            System.out.printf("%-25s %s\n", r.getKey(), r.getValue() ? "✅ OK" : "❌ ERROR");
        }

        System.out.println("\n✔ Exitosos: " + resultados.values().stream().filter(b -> b).count() +
                " / " + resultados.size());

        boolean algunaFallo = resultados.values().stream().anyMatch(val -> !val);
        System.exit(algunaFallo ? 1 : 0);
    }

    // ==== MÉTODOS DE PRUEBA ====

    private static boolean testAgregarAlInicio(ListaEnlazadaTareas lista) {
        try {
            lista.agregarAlInicio(new Tarea("Inicio", "2024-01-01"));
            Nodo cabeza = lista.getCabeza();
            return cabeza != null && cabeza.getTarea().getDescripcion().equals("Inicio");
        } catch (Exception e) {
            System.err.println("Error en testAgregarAlInicio: " + e.getMessage());
            return false;
        }
    }

    private static boolean testAgregarAlFinal(ListaEnlazadaTareas lista) {
        try {
            lista.agregarAlFinal(new Tarea("Final", "2024-01-02"));
            Nodo actual = lista.getCabeza();
            while (actual.getSiguiente() != null) {
                actual = actual.getSiguiente();
            }
            return actual.getTarea().getDescripcion().equals("Final");
        } catch (Exception e) {
            System.err.println("Error en testAgregarAlFinal: " + e.getMessage());
            return false;
        }
    }

    private static boolean testContiene(ListaEnlazadaTareas lista) {
        try {
            return lista.contiene("Inicio");
        } catch (Exception e) {
            System.err.println("Error en testContiene: " + e.getMessage());
            return false;
        }
    }

    private static boolean testEliminar(ListaEnlazadaTareas lista) {
        try {
            return lista.eliminar("Inicio");
        } catch (Exception e) {
            System.err.println("Error en testEliminar: " + e.getMessage());
            return false;
        }
    }

    private static boolean testImprimir(ListaEnlazadaTareas lista) {
        try {
            if (lista.getCabeza() == null) {
                lista.agregarAlInicio(new Tarea("Temporal", "2024-12-31"));
            }

            java.io.ByteArrayOutputStream salida = new java.io.ByteArrayOutputStream();
            java.io.PrintStream original = System.out;
            System.setOut(new java.io.PrintStream(salida));

            lista.imprimir();

            System.setOut(original);

            String output = salida.toString().toLowerCase();
            return output.contains("temporal") || output.contains("final") || output.contains("inicio");

        } catch (Exception e) {
            System.err.println("Error en testImprimir: " + e.getMessage());
            return false;
        }
    }

    private static boolean testBuscarIndice(ListaEnlazadaTareas lista) {
        try {
            return lista.buscarIndice("Final") >= 0;
        } catch (Exception e) {
            System.err.println("Error en testBuscarIndice: " + e.getMessage());
            return false;
        }
    }

    private static boolean testActualizarEstado(ListaEnlazadaTareas lista) {
        try {
            lista.actualizarEstado("Final", "Hecho");
            Nodo n = lista.getCabeza();
            while (n != null) {
                if (n.getTarea().getDescripcion().equals("Final"))
                    return n.getTarea().getEstado().equals("Hecho");
                n = n.getSiguiente();
            }
            return false;
        } catch (Exception e) {
            System.err.println("Error en testActualizarEstado: " + e.getMessage());
            return false;
        }
    }

   private static boolean testFormulario() {
    if (GraphicsEnvironment.isHeadless()) {
        System.out.println("🛈 Entorno headless detectado. Se omite prueba Swing.");
        return true;
    }
    try {
        SwingUtilities.invokeAndWait(() -> {
            VistaTareasFormulario vista = new VistaTareasFormulario();
            new ControladorTareas(vista);
        });
        return true;
    } catch (Exception e) {
        System.err.println("Error en testFormulario: " + e.getMessage());
        return false;
    }
}

        
}
