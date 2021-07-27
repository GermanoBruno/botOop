package com.example.demo;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.LocalTime;
import java.util.List;

@Data
@Document
public class Evento {
    @Id
    private String id;
    private String nome;
    private List<DiaDaSemana> dias_da_semana;
    private LocalTime nao_antes;
    private LocalTime nao_depois;
    private List<Pessoa> pessoas;

    public Evento(String nome, List<DiaDaSemana> dias_da_semana, LocalTime nao_antes, LocalTime nao_depois, List<Pessoa> pessoas) {
        this.nome = nome;
        this.dias_da_semana = dias_da_semana;
        this.nao_antes = nao_antes;
        this.nao_depois = nao_depois;
        this.pessoas = pessoas;
    }
}
