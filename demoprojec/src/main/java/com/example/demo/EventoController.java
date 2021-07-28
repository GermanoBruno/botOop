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

            List<Pessoa> pessoas = event.getPessoas();

            for (int i = 0; i < pessoas.size();i++){
                if (pessoa.getNome().equals(pessoas.get(i).getNome())){
                    throw new Exception("Pessoa ja adicionada");
                }
            }

            for (int i = 0; i < pessoa.getHoras_dosponiveis().size();i++){
                if (! event.getDias_da_semana().contains(pessoa.getHoras_dosponiveis().get(i).getDia())){
                    throw new Exception("Dia da semana inválido");
                }
                for (int j = 0; j < pessoa.getHoras_dosponiveis().get(i).getHorarios().size();j++){
                    if (pessoa.getHoras_dosponiveis().get(i).getHorarios().get(j).compareTo(event.getNao_antes()) < 0 || pessoa.getHoras_dosponiveis().get(i).getHorarios().get(j).compareTo(event.getNao_depois()) > 0){
                        throw new Exception("Horario inválido");
                    }
                }

            }

            return repo.save(event);
        }else{

            throw new Exception("Evento não encontrado");
        }
    }

    @PutMapping("/evento/{id}/updatehorarios/{nomePessoa}")
    public Evento updatePessoaEvento(@RequestBody Pessoa pessoa,@PathVariable String id,@PathVariable String nomePessoa) throws Exception {
        if (repo.findById(id).isPresent()){
            Evento event = repo.findById(id).get();

            List<Pessoa> pessoas = event.getPessoas();
            boolean flagEncontrou = false;

            for (int i = 0; i < pessoas.size();i++){
                if (nomePessoa.equals(pessoas.get(i).getNome())){
                    for (int k = 0; k < pessoa.getHoras_dosponiveis().size();k++){
                        if (! event.getDias_da_semana().contains(pessoa.getHoras_dosponiveis().get(k).getDia())){
                            throw new Exception("Dia da semana inválido");
                        }
                        for (int j = 0; j < pessoa.getHoras_dosponiveis().get(k).getHorarios().size();j++){
                            if (pessoa.getHoras_dosponiveis().get(k).getHorarios().get(j).compareTo(event.getNao_antes()) < 0 || pessoa.getHoras_dosponiveis().get(k).getHorarios().get(j).compareTo(event.getNao_depois()) > 0){
                                throw new Exception("Horario inválido");
                            }
                        }

                    }
                    pessoas.set(i,pessoa);
                    flagEncontrou = true;
                }
            }

            if (!flagEncontrou){
                throw new Exception("Pessoa não encontrada");
            }

            event.setPessoas(pessoas);

            return repo.save(event);
        }else{

            throw new Exception("Evento não encontrado");
        }
    }


}
