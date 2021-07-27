package com.example.demo;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.time.LocalTime;
import java.util.List;

@Data
@AllArgsConstructor
public class DataDisponivel {
    DiaDaSemana dia;
    List<LocalTime> horarios;
}
