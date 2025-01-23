function [u] = Q_Learner_funciton_two(memory_number_of_machine,memory_number_of_task,memory_V_Machine,memory_V_Tasks,memory_dead_lines,itr,unused_task_memory)
    
    Q_table={};
    Q_table_all={};
    k=1;
    kk=1;
    number_of_unused_task_memory=length(unused_task_memory);
    
    for i=1:itr

        selection = randperm(memory_number_of_machine,number_of_unused_task_memory);

        n_selection = size(selection,2);
        
        virtual_M_Used = zeros(1,memory_number_of_machine);
        a = zeros(1,memory_number_of_machine);
        b = zeros(1,memory_number_of_machine);
        
        for ii=1:n_selection
          a(selection(ii))=memory_V_Tasks(unused_task_memory(ii))/memory_V_Machine(selection(ii));
          b(selection(ii))=memory_dead_lines(unused_task_memory(ii));
          virtual_M_Used(selection(ii)) =unused_task_memory(ii);
        end
                
        RMSE = sum(a - b);
        
        Q_table_all(kk,:)={virtual_M_Used,a,b,RMSE};
        kk=kk+1;
        
        if i==1
            Q_table(1,:)={virtual_M_Used,a,b,RMSE};
            k=k+1;
        elseif (i~=1)&&(RMSE< cell2mat(Q_table(k-1,4)))
            Q_table(k,:)={virtual_M_Used,a,b,RMSE};
            k=k+1;
        end
    end
    u={Q_table_all,Q_table,cell2mat(Q_table(end,1)),cell2mat(Q_table(end,2)),cell2mat(Q_table(end,3)),cell2mat(Q_table(end,4))};
