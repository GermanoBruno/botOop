package com.example.demo;

import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@AllArgsConstructor
public class EventoController {
    EventoRepository repo;

    @GetMapping("/eventos")
    public List<Evento> getAllEventos(){
        return repo.findAll();
    }

    @PostMapping("/evento")
    public Evento saveEvento(@RequestBody Evento evento){
        return repo.save(evento);
    }

}
