#include "ec_base_vsx.h"

void gf_3vect_dot_prod_vsx(int len, int vlen, unsigned char *gftbls,
			   unsigned char **src, unsigned char **dest)
{
	unsigned char *s, *t0, *t1, *t2;
	vector unsigned char vX1, vX2, vX3, vX4;
	vector unsigned char vY1, vY2, vY3, vY4, vY5, vY6;
	vector unsigned char vYD, vYE, vYF, vYG, vYH, vYI;
	vector unsigned char vhi0, vlo0, vhi1, vlo1, vhi2, vlo2;
	int i, j, head;

	if (vlen < 128) {
		gf_vect_mul_vsx(len, &gftbls[0 * 32 * vlen], src[0], (unsigned char *)dest[0]);
		gf_vect_mul_vsx(len, &gftbls[1 * 32 * vlen], src[0], (unsigned char *)dest[1]);
		gf_vect_mul_vsx(len, &gftbls[2 * 32 * vlen], src[0], (unsigned char *)dest[2]);

		for (j = 1; j < vlen; j++) {
			gf_3vect_mad_vsx(len, vlen, j, gftbls, src[j], dest);
		}
		return;
	}

	t0 = (unsigned char *)dest[0];
	t1 = (unsigned char *)dest[1];
	t2 = (unsigned char *)dest[2];

	head = len % 64;
	if (head != 0) {
		gf_vect_dot_prod_base(head, vlen, &gftbls[0 * 32 * vlen], src, t0);
		gf_vect_dot_prod_base(head, vlen, &gftbls[1 * 32 * vlen], src, t1);
		gf_vect_dot_prod_base(head, vlen, &gftbls[2 * 32 * vlen], src, t2);
	}

	for (i = head; i < len - 63; i += 64) {
		vY1 = vY1 ^ vY1;
		vY2 = vY2 ^ vY2;
		vY3 = vY3 ^ vY3;
		vY4 = vY4 ^ vY4;
		vY5 = vY5 ^ vY5;
		vY6 = vY6 ^ vY6;

		vYD = vYD ^ vYD;
		vYE = vYE ^ vYE;
		vYF = vYF ^ vYF;
		vYG = vYG ^ vYG;
		vYH = vYH ^ vYH;
		vYI = vYI ^ vYI;

		unsigned char *g0 = &gftbls[0 * 32 * vlen];
		unsigned char *g1 = &gftbls[1 * 32 * vlen];
		unsigned char *g2 = &gftbls[2 * 32 * vlen];

		for (j = 0; j < vlen; j++) {
			s = (unsigned char *)src[j];
			vX1 = vec_xl(0, s + i);
			vX2 = vec_xl(16, s + i);
			vX3 = vec_xl(32, s + i);
			vX4 = vec_xl(48, s + i);

			vlo0 = EC_vec_xl(0, g0);
			vhi0 = EC_vec_xl(16, g0);
			vlo1 = EC_vec_xl(0, g1);
			vhi1 = EC_vec_xl(16, g1);

			vY1 = vY1 ^ EC_vec_permxor(vhi0, vlo0, vX1);
			vY2 = vY2 ^ EC_vec_permxor(vhi0, vlo0, vX2);
			vYD = vYD ^ EC_vec_permxor(vhi0, vlo0, vX3);
			vYE = vYE ^ EC_vec_permxor(vhi0, vlo0, vX4);

			vlo2 = vec_xl(0, g2);
			vhi2 = vec_xl(16, g2);

			vY3 = vY3 ^ EC_vec_permxor(vhi1, vlo1, vX1);
			vY4 = vY4 ^ EC_vec_permxor(vhi1, vlo1, vX2);
			vYF = vYF ^ EC_vec_permxor(vhi1, vlo1, vX3);
			vYG = vYG ^ EC_vec_permxor(vhi1, vlo1, vX4);

			vY5 = vY5 ^ EC_vec_permxor(vhi2, vlo2, vX1);
			vY6 = vY6 ^ EC_vec_permxor(vhi2, vlo2, vX2);
			vYH = vYH ^ EC_vec_permxor(vhi2, vlo2, vX3);
			vYI = vYI ^ EC_vec_permxor(vhi2, vlo2, vX4);

			g0 += 32;
			g1 += 32;
			g2 += 32;
		}

		vec_xst(vY1, 0, t0 + i);
		vec_xst(vY2, 16, t0 + i);
		vec_xst(vY3, 0, t1 + i);
		vec_xst(vY4, 16, t1 + i);
		vec_xst(vY5, 0, t2 + i);
		vec_xst(vY6, 16, t2 + i);

		vec_xst(vYD, 32, t0 + i);
		vec_xst(vYE, 48, t0 + i);
		vec_xst(vYF, 32, t1 + i);
		vec_xst(vYG, 48, t1 + i);
		vec_xst(vYH, 32, t2 + i);
		vec_xst(vYI, 48, t2 + i);
	}
	return;
}
