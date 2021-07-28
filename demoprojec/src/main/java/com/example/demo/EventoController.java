package com.example.demo;

import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;

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

    @GetMapping("/evento/{id}")
    public Evento getEventoById(@PathVariable String id){
        return repo.findById(id).get();
    }

    @DeleteMapping("/evento/{id}")
    public void deleteEventoById(@PathVariable String id){
        repo.deleteById(id);
    }

    @PutMapping("/evento/{id}")
    public Evento updateEvento(@RequestBody Evento evento,@PathVariable String id) throws Exception {
        if (repo.findById(id).isPresent()){
            return repo.save(evento);
        }else{
            throw new Exception("Evento não encontrado");
        }
    }


    @PostMapping("/evento/{id}/inserePessoa")
    public Evento addPessoaEvento(@RequestBody Pessoa pessoa,@PathVariable String id) throws Exception {
        if (repo.findById(id).isPresent()){
            Evento event = repo.findById(id).get();
            event.getPessoas().add(pessoa);
            return repo.save(event);
        }else{

            throw new Exception("Evento não encontrado");
        }
    }
    


}
