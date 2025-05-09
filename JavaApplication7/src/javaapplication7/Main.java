/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package javaapplication7;

/**
 *
 * @author USUARIO
 */
import Laboratorio_Semana07.vista.VistaTareasFormulario;
import Laboratorio_Semana07.controlador.ControladorTareas;

public class Main {
    public static void main(String[] args) {
        VistaTareasFormulario vista = new VistaTareasFormulario();
        new ControladorTareas(vista);
    }
}
