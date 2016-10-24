num_for_each = 100;
x = [-5:0.1:5];
fout = fopen('raw_data.txt','w');
for i = 1:num_for_each
	%SIN 1
	A = rand()+1;
	b = rand()*pi;
	c = rand();
	y = A*sin(x+b)+c;
	for j = 1:size(y,2)
		fprintf(fout,'%4.5f\t',y(j));
	end
	fprintf(fout, '%d\n', 1);
	%LINEAR 2
	A = rand()+1;
	b = rand();
	y = A*x+b;
	for j = 1:size(y,2)
		fprintf(fout,'%4.5f\t',y(j));
	end
	fprintf(fout, '%d\n', 2);
	%QUADRATIC 3
	A = rand()+1;
	b = rand();
	c = rand();
	y = A*(x.*x)+b*x+c;
	for j = 1:size(y,2)
		fprintf(fout,'%4.5f\t',y(j));
	end
	fprintf(fout, '%d\n', 3);
end
fclose(fout);