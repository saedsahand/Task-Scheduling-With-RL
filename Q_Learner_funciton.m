function [u] = Q_Learner_funciton(memory_number_of_machine,memory_number_of_task,memory_V_Machine,memory_V_Tasks,memory_dead_lines,itr,unused_task_memory)
    
    Q_table={};
    Q_table_all={};
    k=1;
    kk=1;
    number_of_unused_task_memory=length(unused_task_memory);
    
    for i=1:itr

        selection = randperm(number_of_unused_task_memory,memory_number_of_machine);

        n_selection = size(selection,2);
        
        for ii=1:n_selection
          a(ii)=memory_V_Tasks(unused_task_memory(selection(ii)))/memory_V_Machine(ii);
        end
        
        b=memory_dead_lines(unused_task_memory(selection));
        
        E = sum(a - b);
        
        Q_table_all(kk,:)={unused_task_memory(selection),a,b,E};
        kk=kk+1;
        
        if i==1
            Q_table(1,:)={unused_task_memory(selection),a,b,E};
            k=k+1;
        elseif (i~=1)&&(E< cell2mat(Q_table(k-1,4)))
            Q_table(k,:)={unused_task_memory(selection),a,b,E};
            k=k+1;
        end
    end
    u={Q_table_all,Q_table,cell2mat(Q_table(end,1)),cell2mat(Q_table(end,2)),cell2mat(Q_table(end,3)),cell2mat(Q_table(end,4))};
