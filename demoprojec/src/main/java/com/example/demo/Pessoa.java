package com.example.demo;

import lombok.AllArgsConstructor;
import lombok.Data;


import java.util.List;

@Data
@AllArgsConstructor
class Pessoa {
        String nome ;
        List<DataDisponivel> horas_dosponiveis;
}
