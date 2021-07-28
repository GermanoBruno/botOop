package com.example.demo;

import java.util.Date;

class Pessoa {
        String nome ;
        Date horas_dosponiveis[];

    public Pessoa(String nome, Date[] horas_dosponiveis) {
        this.nome = nome;
        this.horas_dosponiveis = horas_dosponiveis;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public void setHoras_dosponiveis(Date[] horas_dosponiveis) {
        this.horas_dosponiveis = horas_dosponiveis;
    }

    public String getNome() {
        return nome;
    }

    public Date[] getHoras_dosponiveis() {
        return horas_dosponiveis;
    }
}
