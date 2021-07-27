package com.example.demo;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.time.LocalTime;
import java.util.List;

@SpringBootApplication
public class DemoApplication {

    public static void main(String[] args) {

        SpringApplication.run(DemoApplication.class, args);

    }

    @Bean
    CommandLineRunner runner(EventoRepository repo){
        return args -> {
            DataDisponivel d1 = new DataDisponivel(DiaDaSemana.SEG, List.of(LocalTime.of(12,0,0)));
            Pessoa p1 = new Pessoa("Tutu",List.of(d1));
            Evento evento = new Evento("REUNIÃO POO",
                    List.of(DiaDaSemana.SEG,DiaDaSemana.QUA,DiaDaSemana.SEX),
                    LocalTime.of(8,00),
                    LocalTime.of(18,0),
                    List.of(p1));

            repo.insert(evento);
        };
    }
}
